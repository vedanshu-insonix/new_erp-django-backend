from rest_framework import viewsets
from system import utils
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters
from system.models.common import FormData, FormList, List
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

def response_function(key, sp):
    text = key.split('__')
    new_key = text[sp]
    if new_key != 'id': return new_key
    else: return key

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

    print(colRec)
    return tableName, valueList

class GlobalViewsets(viewsets.ViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    def retrieve(self, request, pk=None):
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

        return Response({"message": resData,
                    "status" : "success",
                    "code"   : status.HTTP_201_CREATED})