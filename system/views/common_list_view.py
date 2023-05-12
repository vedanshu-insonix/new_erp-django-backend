from rest_framework import viewsets
from system import utils
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters
from system.models.common import FormData, FormList, List, Choice
from sales.serializers.customers_serializers import *
from django.core import serializers
import json
from system.models.dataset import SchemaRelation
import threading
from system.models.teams import Team,TeamUser
from system.models.roles_permissions import Permission,RolePermissions,RoleCategories,Role,RoleTerritories
from sales.models.carts import Carts
from sales.models.returns import  SalesReturnLines
from sales.models.sales_credit import SalesCredits
from sales.models.quotations import SalesQuotations
from sales.models.sales_orders import SalesOrders
from sales.models.invoices import SalesInvoices
from sales.models.receipts import Receipts
from sales.models.returns import SalesReturns
from sales.models.vendors import VendorPrices


def check_parenthesis(self, query):
    stack = list()
    for i in query:
        if i == '(': stack.append('(')
        elif i == ')': stack.pop()
    return stack

def response_function(key, sp):
    text = key.split('__')
    if len(text)>1: 
        new_key = text[sp]
        if new_key != 'id':return new_key
    return key

def get_column(schema, lid, fd):
    tableName = ""
    valueList = ['id']
    dataList = fd.filter(table=schema['table'])
    newData = dataList.values('data__id')
    newDataList = [d['data__id'] for d in newData]
    colRec = Column.objects.filter(Q(col_list=lid), Q(col_data__in=newDataList), 
                                        (Q(visibility__system_name__icontains='Required')|Q(visibility__system_name__icontains='Default')))
    if colRec:
        tableName = dataList[0].table.link_source
        for rec in colRec:
            field = rec.col_data.field
            if rec.col_data.linked_data:
                field = field+"__"+rec.col_data.linked_data.field
            valueList.append(field)
    return tableName, valueList

def get_model_fields(modelName):
    fld = f'{modelName}._meta.get_fields()'
    fld = eval(fld)
    fields = [f.name for f in fld]
    return fields

def filter_query(lid, primarySchema, rt):
    default_filter = ListFilters.objects.filter(list=lid, default=True).order_by('sequence')
    if default_filter:
        query = ".filter("
        fList = []

        primaryFields = get_model_fields(primarySchema)
        relatedFields = {}

        for tbl in rt:
            tableName = rt[tbl]
            relatedFields[tbl] = get_model_fields(tableName)

        for flt in default_filter: 
            fDict = {}

            fLogic = flt.logic
            if fLogic: fLogic = fLogic.system_name   
            fDict['logic']=fLogic

            fData=flt.data.field
            if fData in primaryFields:
                print("")
            else:
                for tbl in relatedFields:
                    if fData in relatedFields[tbl]:
                        prefix = tbl
                        fData = prefix+"__"+fData
            if flt.data.linked_data: fData=fData+"__"+flt.data.linked_data.field
            fDict['data']=fData

            fOp = flt.operator
            if fOp: fOp = fOp.system_name    
            fDict['operator']=fOp

            fDict['value']=flt.value

            fsublogic = flt.sublogic
            if fsublogic: fsublogic = fsublogic.system_name
            fDict['sublogic']=fsublogic

            fList.append(fDict)

        for i in range(len(fList)):
            op = fList[i]['operator']
            field = fList[i]['data']
            value = fList[i]['value']
            sublogic = fList[i]['sublogic']

            if op == 'is' or op == 'is_not': lookup = "%s" % field
            if op == 'is_greater': lookup = "%s__gt" % field
            if op == 'is_less': lookup = "%s__lt" % field
            if op == 'is_greaterthan_or_equal': lookup = "%s__gte" % field
            if op == 'is_lessthan_or_equal': lookup = "%s__lte" % field

            if fList[i] == fList[-1]:
                if op == 'is_not': new_query = "~Q("+lookup+"='"+value+"')"
                else: new_query = "Q("+lookup+"='"+value+"')"
                if new_query in query:
                    sq = check_parenthesis(query)
                    if sq:
                        for i in range(len(sq)):
                            subquery = query+')'
                else: 
                    subquery = query+new_query+")"
            else:
                if sublogic:
                    op1 = fList[i+1]['operator']
                    field1 = fList[i+1]['column']
                    value1 = fList[i+1]['value']

                    if op == 'is_not': sub1 = "~Q("+lookup+"='"+value+"')"
                    else: sub1 = "Q("+lookup+"='"+value+"')"

                    if op1 == 'is' or op1 == 'is_not': lookup1 = "%s" % field1
                    if op1 == 'is_greater': lookup1 = "%s__gt" % field1
                    if op1 == 'is_less': lookup1 = "%s__lt" % field1
                    if op1 == 'is_greaterthan_or_equal': lookup1 = "%s__gte" % field1
                    if op1 == 'is_lessthan_or_equal': lookup1 = "%s__lte" % field1

                    if op1 == 'is_not': sub2 = "~Q("+lookup1+"='"+value1+"')"
                    else: sub2 = "Q("+lookup1+"='"+value1+"')"

                    if sublogic =='and': subquery = query+"("+sub1+","+sub2+")"
                    elif sublogic == 'or': subquery = query+"("+sub1+"|"+sub2+")"
                else:    
                    if op == 'is_not': subquery = query+"~Q("+lookup+"='"+value+"')"
                    else: subquery = query+"Q("+lookup+"='"+value+"')"

                logic = fList[i+1]['logic']
                if logic == 'and': subquery = subquery + ","
                elif logic == 'or': subquery = subquery + "|"
                else: print("Logic >", logic)
            query = subquery
            print(query)
        return query
    return None

def sort_query(lid):
    default_order = ListSorts.objects.filter(list=lid, default=True).order_by('sequence')
    print("demo >>>>>>>>>",default_order)
    if default_order:
        query = ".order_by("
        oList = []

        for orders in default_order: 
            oDict = {}

            oCol = orders.column
            if oCol: oCol = oCol.col_data.field 
            oDict['column']=oCol

            oDirec=orders.sort_direction
            if oDirec:
                direc = Choice.objects.get(id=oDirec)
                oDirec = direc.system_name
            oDict['direction']=oDirec
            
            oList.append(oDict)

        for i in range(len(oList)):
            col = oList[i]['column']
            dr = oList[i]['direction']
            grp = oList[i]['grouping']

            if dr == 'descending':
                subQuery = query+"-'"+col+"'"
            else:
                subQuery = query+"'"+col+"'"
            if oList[i] == oList[-1]:
                subQuery = subQuery + ')'
            else:
                subQuery = subQuery + ','
            query = subQuery
        return query
    return None

class GlobalViewsets(viewsets.ViewSet):

    """def retrieve(self, request, pk=None):
        lid = request.GET.get('l')
        primarySchema = List.objects.get(id=lid).data_source.link_source
        formData = FormData.objects.filter(form=pk)
        uniqueTable = formData.values('table').distinct()
        relatedSchema = []
        relSchemaField = []
        resData = []
        primaryIds = []
        for x in uniqueTable:
            schemaField = {}
            tableName, valueList = get_column(x, lid, formData)
            if tableName != "" and tableName == primarySchema:
                listQuery = tableName + ".objects.all()"
                listData = eval(listQuery)
                resData = listData.values(*valueList)
                for res in resData:
                    for key in valueList:
                        new_key = response_function(key, 0)
                        if new_key!=key:
                            v1 = res[key]
                            res.pop(key)
                            res[new_key]=v1
                primaryIds = listData.values('id')
            if tableName != "" and tableName != primarySchema:
                relatedSchema.append(tableName)
                schemaField[tableName] = valueList
                relSchemaField.append(schemaField)
        for schema in relatedSchema:
            relData = SchemaRelation.objects.filter(primary = primarySchema , related=schema).first()
            primaryFieldName = relData.primary_field
            relFieldName = relData.related_field
            relSchema = relData.relation
            prField = relData.primay_rec_field
            isPr = relData.primay_rec
            schRelField = [d[schema] for d in relSchemaField if schema in d][0]
            schRelFieldConcat = [relFieldName + "__" + s for s in schRelField]
            
            for id in primaryIds:
                relPrimaryData = [d for d in resData if d['id'] == id['id']][0]
                if isPr:
                    getRelData = relSchema + ".objects.filter("+primaryFieldName+"='"+id['id']+"',"+relFieldName+"__"+prField+"=True)"
                else:
                    getRelData = relSchema + ".objects.filter("+primaryFieldName+"='"+id['id']+"')"
                relatedSchemaData = eval(getRelData)
                relatedSchemaData = relatedSchemaData.values(*schRelFieldConcat)
                if relatedSchemaData:
                    for key, value in relatedSchemaData[0].items():
                        new_key = response_function(key, 1)
                        relPrimaryData[new_key]=value
                else:
                    for rec in schRelField:
                        new_key = response_function(rec, 0)
                        if rec != 'id':
                            relPrimaryData[new_key]= None
        lf = ListFilters.objects.filter(list=lid)
        print(lf)
        return Response({"message": resData,
                    "status" : "success",
                    "code"   : status.HTTP_201_CREATED})"""
    
    def retrieve(self, request, pk=None):
        lid = request.GET.get('l')
        primarySchema = List.objects.get(id=lid).data_source.link_source
        formData = FormData.objects.filter(form=pk)
        uniqueTable = formData.values('table').distinct()
        relatedSchema = []
        relatedRecIds = {}
        relSchemaField = []
        resData = []
        primaryIds = []
        typeList = ['ManyToManyField', 'OneToOneField']
        rt = {}
        for x in uniqueTable:
            schemaField = {}
            tableName, valueList = get_column(x, lid, formData)
            
            if tableName != "" and tableName == primarySchema:
                relModel = f'{tableName}._meta.get_fields()'
                relModel = eval(relModel)
                for f in relModel:
                    if f.get_internal_type() in typeList: 
                        fieldName = f.name
                        relatedTo = f.related_model.__name__
                        rt[fieldName]=relatedTo
                listQuery = f'{tableName}.objects.all()'
                # adding default filter feature
                filteredResult = filter_query(lid, primarySchema, rt)
                if filteredResult:
                    listQuery = listQuery+filteredResult+".distinct()"
                # adding default sort feature
                orderResult = sort_query(lid)
                print(orderResult)
                if orderResult:
                    listQuery = listQuery+orderResult
                listData = eval(listQuery)
                resData = listData.values(*valueList)
                for d in listData:
                    recId = d.id
                    for fields in rt:
                        rid = []
                        table = rt[fields]
                        new = f'{tableName}.objects.get(id="{recId}").{fields}.all()'
                        relIds = eval(new)
                        for rec in relIds:
                            rid.append(rec.id)
                        data = {table:rid}
                        relatedRecIds[recId] = data
                for res in resData:
                    for key in valueList:
                        new_key = response_function(key, 0)
                        if new_key!=key:
                            v1 = res[key]
                            res.pop(key)
                            res[new_key]=v1
                primaryIds = listData.values('id')
            if tableName != "" and tableName != primarySchema:
                relatedSchema.append(tableName)
                schemaField[tableName] = valueList
                relSchemaField.append(schemaField)
        
        for schema in relatedSchema:
            schRelField = [d[schema] for d in relSchemaField if schema in d][0]

            for id in primaryIds:
                relPrimaryData = [d for d in resData if d['id'] == id['id']][0]
                recnumber = relatedRecIds[id['id']]
                rid = recnumber[schema]
                if len(rid) > 1:
                    r = f'{schema}.objects.filter(id__in={rid}, default=True)'
                else:
                    r = f'{schema}.objects.filter(id__in={rid})'
                relatedSchemaData = eval(r)
                relatedSchemaData = relatedSchemaData.values(*schRelField)
                if relatedSchemaData:
                    for key, value in relatedSchemaData[0].items():
                        new_key = response_function(key, 0)
                        if new_key == 'id':
                            new_key = schema+"_"+new_key
                        relPrimaryData[new_key]=value
                else:
                    for rec in schRelField:
                        new_key = response_function(rec, 0)
                        if rec == 'id':
                            new_key = schema+"_"+rec
                        relPrimaryData[new_key]= "---"
                print(relPrimaryData)
        return Response({"message": resData,
                    "status" : "success",
                    "code"   : status.HTTP_201_CREATED})
    
class FeatureViewsets(viewsets.ViewSet):

    # Clone an existing record of an model. 
    def create(self, request):
        recId = request.data.get('rec_id')
        listId = request.GET.get('l')
        if recId and listId:
            primarySchema = List.objects.get(id=listId).data_source.link_source
            oldRec = f'{primarySchema}.objects.get(id="{recId}")'
            oldRec = eval(oldRec)
            # relRec = oldRec.address.all()
            oldRec.id = get_rid_pkey((primarySchema.lower()))
            oldRec._state.adding = True
            oldRec.save()
            # oldRec.address.set(relRec)
        return Response({"message": "success",
                    "status" : "success",
                    "code"   : status.HTTP_201_CREATED})
