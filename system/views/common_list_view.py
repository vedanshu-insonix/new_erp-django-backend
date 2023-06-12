from rest_framework import viewsets
from system import utils
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from system.models import *
from system.service import get_rid_pkey, get_related_pkey
from sales.models import *
from warehouse.models import *
from purchasing.models import *

childModels = ['Choice', 'State', 'Data']

# check the EOF of a static query.
def check_parenthesis(self, query):
    stack = list()
    for i in query:
        if i == '(': stack.append('(')
        elif i == ')': stack.pop()
    return stack

# adjusting the key name as per requirement in response dict.
def response_function(key, sp):
    text = key.split('__')
    if len(text)>1: 
        new_key = text[sp]
        if new_key != 'id':return new_key
    return key

# getting the name of fields to be send in get response.
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

# get all the field name of a model.
def get_model_fields(modelName):
    fld = f'{modelName}._meta.get_fields()'
    fld = eval(fld)
    fields = [f.name for f in fld]
    return fields

# get the field name of m2m and o2o type in model.
def get_m2m_fields(modelName):
    rt = {}
    typeList = ['ManyToManyField', 'OneToOneField']
    relModel = f'{modelName}._meta.get_fields()'
    relModel = eval(relModel)
    for f in relModel:
        if f.get_internal_type() in typeList: 
            fieldName = f.name
            relatedTo = f.related_model.__name__
            rt[relatedTo] = fieldName

    return rt

# create default filter query for each list as a string.
def filter_query(lid, primarySchema):
    default_filter = ListFilters.objects.filter(list=lid, default=True).order_by('sequence')
    if default_filter:
        query = ".filter("
        fList = []
        rt = get_m2m_fields(primarySchema)

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
            if fData not in primaryFields:
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

# create default sort query for each list as a string.
def sort_query(lid):
    default_order = ListSorts.objects.filter(list=lid, default=True).order_by('sequence')
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
            #grp = oList[i]['grouping']

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

    # global get api. -------------------------->(under testing)
    def list(self, request):
        lid = request.GET.get('l')
        formId = request.GET.get('f')
        primarySchema = List.objects.get(id=lid).data_source.link_source
        formData = FormData.objects.filter(form=formId)
        uniqueTable = formData.values('table').distinct()
        relatedSchema = []
        relSchemaField = []
        resData = []
        primaryIds = []
        for x in uniqueTable:
            schemaField = {}
            tableName, valueList = get_column(x, lid, formData)
            if tableName != "" and tableName == primarySchema:
                listQuery = f'{tableName}.objects.all()'
                # adding default filter feature
                filteredResult = filter_query(lid, primarySchema)
                if filteredResult:
                    listQuery = listQuery+filteredResult+".distinct()"
                # adding default sort feature
                orderResult = sort_query(lid)
                if orderResult:
                    listQuery = listQuery+orderResult
                # get data.
                listData = eval(listQuery)
                resData = listData.values(*valueList)
                
                # to return valid keys.
                for res in resData:
                    for key in valueList:
                        new_key = response_function(key, 0)
                        if new_key!=key:
                            v1 = res[key]
                            res.pop(key)
                            res[new_key]=v1
                primaryIds = listData.values('id')
            elif tableName != "" and tableName != primarySchema:
                relatedSchema.append(tableName)
                schemaField[tableName] = valueList
                relSchemaField.append(schemaField)
        for schema in relatedSchema:
            relatedFields = get_m2m_fields(schema)
            schRelField = [d[schema] for d in relSchemaField if schema in d][0]
            for id in primaryIds:
                relPrimaryData = [d for d in resData if d['id'] == id['id']][0]
                filterField = relatedFields[primarySchema]
                getRelData = f'{schema}.objects.filter({filterField}="{id["id"]}", default=True)'
                getRelData = eval(getRelData)
                if getRelData:
                    relatedSchemaData = getRelData
                else:
                    getRelData = f'{schema}.objects.filter({filterField}="{id["id"]}")'
                    relatedSchemaData = eval(getRelData)
                relatedSchemaData = relatedSchemaData.values(*schRelField)
                if relatedSchemaData:
                    for key, value in relatedSchemaData[0].items():
                        new_key = response_function(key, 0)
                        if new_key == 'id':
                            new_key = schema+"__"+new_key
                        relPrimaryData[new_key]=value
                else:
                    for rec in schRelField:
                        new_key = response_function(rec, 0)
                        if rec == 'id':
                            new_key = schema.lower()+"__"+rec
                        relPrimaryData[new_key]= "---"
        return Response({"message": resData,
                    "status" : "success",
                    "code"   : status.HTTP_201_CREATED})

    # global create api. ----------------->(under testing)
    def create(self, request):
        listId = request.GET.get('l')
        formId = request.GET.get('f')
        getData = request.data
        primaryTable = List.objects.get(id=listId).data_source.link_source 
        formData = FormData.objects.filter(form=formId)
        uniqueTable = formData.values('table').distinct()
        primaryM2M = get_m2m_fields(primaryTable)
        m2mFields = [primaryM2M[mod] for mod in primaryM2M]
        m2mData = []

        # create record in primary model.
        primaryFields = get_model_fields(primaryTable)
        primaryQuery = f'{primaryTable}.objects.create('
        for data in formData:
            fld = data.data.field
            if fld in m2mFields:
                m2mData.append(fld)
                pass
            elif (fld in getData) and (fld in primaryFields):
                fieldData = getData.get(fld)
                if data.data.linked_ds:
                    lookupModel = data.data.linked_ds.link_source
                    val = f'{lookupModel}.objects.filter(id="{fieldData}").first()'
                    fVal = eval(val)
                    if fVal:
                        fieldData = fVal.id
                    subQuery = f'{primaryQuery} {fld}_id = "{fieldData}",'
                else:
                    subQuery = f'{primaryQuery} {fld} = "{fieldData}",'
                primaryQuery = subQuery
        primaryID = get_rid_pkey(primaryTable.lower())
        primaryQuery = primaryQuery+"id = '"+primaryID+"')"
        primaryResult = eval(primaryQuery)
        
        # add m2m field data.
        for data in m2mData:
            modelName = ''
            for models in primaryM2M:
                if primaryM2M[models] == data:
                    modelName = models
                    break
            toAdd = getData.get(data)
            getRelated = get_m2m_fields(modelName)
            relFld = getRelated[primaryTable]
            try:
                m2mQuery = f'{modelName}.objects.get(id="{toAdd}").{relFld}.add("{primaryID}")'
                res = eval(m2mQuery)
            except:
                pass

        # create record in related models.
        for x in uniqueTable:
            tableName = DataTable.objects.get(id=x['table'])
            tableName = tableName.link_source
            
            if tableName != '' and tableName != primaryTable:
                rField = get_m2m_fields(tableName)
                pRelField = rField[primaryTable]
                relQuery = f'{tableName}.objects.create('
                modelFields = get_model_fields(tableName)
                for data in formData:
                    fld = data.data.field
                    if fld != pRelField:
                        if (fld in getData) and (fld in modelFields):
                            fieldData = getData.get(fld)
                            if data.data.linked_ds:
                                lookupModel = data.data.linked_ds.link_source
                                val = f'{lookupModel}.objects.filter(id="{fieldData}").first()'
                                fVal = eval(val)
                                if fVal:
                                    fieldData = fVal.id
                                subQuery = f'{relQuery} {fld}_id = {fieldData},'
                            else:
                                subQuery = f'{relQuery} {fld} = "{fieldData}",'
                            relQuery = subQuery
                    elif fld == pRelField:
                        subQuery = fld+"_id='"+primaryID+"', "
                        relQuery = relQuery + subQuery
                newID = get_rid_pkey(tableName.lower())
                relQuery = relQuery+"id = '"+newID+"')"
                relResult = eval(relQuery)
                
        # Success response.
        return Response(utils.success_msg("Record Creation Successful."))
    
    # global update api. ------------------------>(works fine in forward direction.)(under testing)
    def update(self, request, pk):
        listId = request.GET.get('l')
        formId = request.GET.get('f')
        getData = request.data
        primaryTable = List.objects.get(id=listId).data_source.link_source
        formData = FormData.objects.filter(form=formId)
        initQuery = f'{primaryTable}.objects.get(id="{pk}")'
        oldRec = eval(initQuery)
        uniqueTable = formData.values('table').distinct()
        primaryM2M = get_m2m_fields(primaryTable)

        # Update the records in primary model.
        updateQuery = f'{primaryTable}.objects.filter(id="{pk}").update('
        primaryFields = get_model_fields(primaryTable)
        for data in formData:
            fld = data.data.field
            if (fld in getData) and (fld in primaryFields):
                fieldData = getData.get(fld)
                if data.data.linked_ds:
                    lookupModel = data.data.linked_ds.link_source
                    val = f'{lookupModel}.objects.filter(id="{fieldData}").first()'
                    fVal = eval(val)
                    fieldData = fVal.id
                    subQuery = f'{updateQuery} {fld}_id = {fieldData},'
                else:
                    subQuery = f'{updateQuery} {fld} = "{fieldData}",'
                updateQuery = subQuery
        updateQuery = updateQuery[:-1]+')'
        updateRes = eval(updateQuery)

        # update record in related models.
        for x in uniqueTable:
            tableName = DataTable.objects.get(id=x['table'])
            tableName = tableName.link_source
            rField = get_m2m_fields(tableName)
            pRelField = rField[primaryTable]
            if tableName != '' and tableName != primaryTable:
                relField = rField[primaryTable]
                relTableData = f'{tableName}.objects.filter({relField}="{pk}")'
                relTableData1 = eval(relTableData)

                # if the model have no related data than create new data.
                if len(relTableData1) == 0:
                    relQuery = f'{tableName}.objects.create('
                    modelFields = get_model_fields(tableName)
                    for data in formData:
                        fld = data.data.field
                        if fld != pRelField:
                            if (fld in getData) and (fld in modelFields):
                                fieldData = getData.get(fld)
                                if data.data.linked_ds:
                                    lookupModel = data.data.linked_ds.link_source
                                    val = f'{lookupModel}.objects.filter(id="{fieldData}").first()'
                                    fVal = eval(val)
                                    fieldData = fVal.id
                                    subQuery = f'{relQuery} {fld}_id = {fieldData},'
                                else:
                                    subQuery = f'{relQuery} {fld} = "{fieldData}",'
                                relQuery = subQuery
                        elif fld == pRelField:
                            subQuery = fld+"_id='"+pk+"', "
                            relQuery = relQuery + subQuery
                    newID = get_rid_pkey(tableName.lower())
                    relQuery = relQuery+"id = '"+newID+"')"
                    relResult = eval(relQuery)
                    relFIeld = primaryM2M[tableName]
                # update the existing related model data record.
                else:
                    if len(relTableData1)>1: 
                        relQuery = f'{tableName}.objects.filter(id__in={relTableData}, default=True).update('
                    elif len(relTableData1)==1:
                        relQuery = f'{tableName}.objects.filter(id__in={relTableData}).update('

                    modelFields = get_model_fields(tableName)
                    for data in formData:
                        fld = data.data.field
                        if fld != pRelField:
                            if (fld in getData) and (fld in modelFields):
                                fieldData = getData.get(fld)
                                if data.data.linked_ds:
                                    lookupModel = data.data.linked_ds.link_source
                                    val = f'{lookupModel}.objects.filter(id="{fieldData}").first()'
                                    fVal = eval(val)
                                    fieldData = fVal.id
                                    subQuery = f'{relQuery} {fld}_id = {fieldData},'
                                else:
                                    subQuery = f'{relQuery} {fld} = "{fieldData}",'
                                relQuery = subQuery
                        elif fld == pRelField:
                            subQuery = fld+"_id='"+pk+"', "
                            relQuery = relQuery + subQuery
                    relQuery = relQuery[:-1]+')'
                    relResult = eval(relQuery)

        # Success response.
        return Response(utils.success_msg("Record Updation Successful."))
    
    # global delete api. ------------------->(needs to implement related record deletion feature.)
    def destroy(self, request, pk):
        try:
            listId = request.GET.get('l')
            tableName = List.objects.get(id=listId).data_source.link_source
            deleteQuery = f'{tableName}.objects.get(id="{pk}").delete()'
            result = eval(deleteQuery)
            msg = "Record Deleted Successfully."
            return Response(utils.success_msg(msg))
        except Exception as e:
            return Response(utils.error(str(e)))

    # global get by id api.  -------------------->(in progress)  
    def retrieve(self, request, pk=None):
        lid = request.GET.get('l')
        formID = request.GET.get('f')
        formData = FormData.objects.filter(form=formID)
        uniqueTable = formData.values('table').distinct()
        primaryTable = List.objects.get(id=lid).data_source.link_source
        listQuery = f'{primaryTable}.objects.filter(id="{pk}")'
        result = eval(listQuery)
        primaryFields = get_model_fields(primaryTable)

        valueList = []
        relatedValueList = []
        
        for data in formData:
            if data.data:
                responseKey = data.data.field
                keyType = data.data.field_type
                if responseKey in primaryFields:
                    if keyType == 'foreign key':
                        getData = responseKey+"__"+data.data.linked_data.field
                    elif keyType == 'lookup':
                        getData = responseKey+"__system_name"
                    else:
                        getData = responseKey
                    valueList.append(getData)
        # primary model data.
        result = result.values(*valueList)

        # to return valid keys.
        for res in result:
            for key in valueList:
                new_key = response_function(key, 0)
                if new_key!=key:
                    v1 = res[key]
                    res.pop(key)
                    res[new_key]=v1
        relatedResult = []
        # related model data.
        for x in uniqueTable:
            tableName = DataTable.objects.get(id=x['table'])
            tableName = tableName.link_source
            print(tableName)
            
            rField = get_m2m_fields(tableName)
            pRelField = rField[primaryTable]
            if tableName != '' and tableName != primaryTable:
                # related model fields.
                relFields = get_model_fields(tableName)
                print(relFields)
                for data in formData:
                    if data.data:
                        responseKey = data.data.field
                        keyType = data.data.field_type
                        print("responseKey --->", responseKey)
                        if responseKey in relFields:
                            if keyType == 'foreign key':
                                getData = responseKey+"__"+data.data.linked_data.field
                            elif keyType == 'lookup':
                                getData = responseKey+"__system_name"
                            else:
                                getData = responseKey
                            print("getData --->", getData)
                            relatedValueList.append(getData)
                print("relatedValueList ---->", relatedValueList)
                relField = rField[primaryTable]
                relTableData = f'{tableName}.objects.filter({relField}="{pk}")'
                relTableData1 = eval(relTableData)

                if relTableData1:
                    relatedResult = relTableData1.values(*relatedValueList)
                    for key, value in relatedResult[0].items():
                        new_key = response_function(key, 0)
                        result[0][new_key] = value
                else:
                    for i in range(len(relatedValueList)):
                        key = relatedValueList[i]
                        new_key = response_function(key, 0)
                        result[0][new_key] = '____'
        return Response(utils.success_msg(result))
        
class FeatureViewsets(viewsets.ViewSet):

    # Clone an existing record of a model. 
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
        msg = "Cloning Successful."
        return Response(utils.success_msg(msg))
