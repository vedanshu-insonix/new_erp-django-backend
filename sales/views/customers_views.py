import json
from rest_framework import viewsets
from system import utils
from ..models.customers import Customers, CustomerAddress
from ..models.address import Addresses
from ..serializers.customers_serializers import CustomerSerializer
from ..serializers.addresses_serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters
import openpyxl
from system.models.common import Choice, ListFilters, Currency, FormStage, Stage

def check_parenthesis(self, query):
    stack = list()
    for i in query:
        if i == '(': stack.append('(')
        elif i == ')': stack.pop()
    return stack 

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("__all__")
    filterset_fields = {
            'customer': ['exact', 'icontains'],'entity': ['exact'],'shipping_terms': ['exact'],
            'ship_via': ['exact'],'customer_source': ['exact'],'payment_terms': ['exact'],'payment_method': ['exact'],
            'currency' : ['exact'],'free_freight_minimum' : ['exact', 'contains'],'issue_statements' : ['exact'],
            'require_pos': ['exact'],'credit_limit': ['exact', 'contains'],'account_balance': ['exact', 'contains'],
            'current_orders': ['exact', 'contains'], 'authorised_card': ['exact', 'contains'], 'credit_available': ['exact', 'contains'],
            'overdue': ['exact'],'average_pay_days': ['exact'],'last_credit_review': ['exact'],'credit_hold': ['exact'],
            'customer_receivable_account': ['exact'],'stage': ['exact'],'stage_started': ['exact'],'status': ['exact'], 'used': ['exact']
        }
    ordering_fields = ("__all__")

    def create(self, request, *args, **kwargs):
        try:
            GetData = request.data
            customer_fields = [f.name for f in Customers._meta.get_fields()]
            address_fields = [f.name for f in Addresses._meta.get_fields()]
            customer_data = {}
            address_data = {}
            returnData = {}
            for keys, values in GetData.items():
                if keys in customer_fields:
                    customer_data[keys] = values
                elif keys in address_fields:
                    address_data[keys] = values

            if customer_data:
                serializers = CustomerSerializer(data = customer_data, context={'request': request})
                if serializers.is_valid(raise_exception=True):
                    serializers.save()
                CustomerInstance = Customers.objects.get(id = serializers.data.get("id"))
                if address_data:
                    address_serializers = AddressSerializer(data=address_data, context={'request': request})
                    if address_serializers.is_valid(raise_exception=True):
                        address_serializers.save()
                        
                        # Create Relation between Customer and Address
                        AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                returnData = CustomerSerializer(CustomerInstance, context={'request': request})
                returnData = returnData.data
            return Response(utils.success_msg(returnData))
        except Exception as e:
            return Response(utils.error(str(e)))
   
    def update(self, request, pk=None):
        GetData = request.data
        try:
            CustomerInstance = Customers.objects.get(id=pk)
            customer_fields = [f.name for f in Customers._meta.get_fields()]
            address_fields = [f.name for f in Addresses._meta.get_fields()]
            customer_data = {}
            address_data = {}
            for keys, values in GetData.items():
                if keys in customer_fields:
                    customer_data[keys] = values
                elif keys in address_fields:
                    address_data[keys] = values

            if customer_data:
                serializers = CustomerSerializer(CustomerInstance, data = customer_data, context={'request': request})
                if serializers.is_valid(raise_exception=True):
                    serializers.save()
            if address_data:
                ca_rec=CustomerAddress.objects.filter(customer = CustomerInstance).values('address')
                if ca_rec:
                    address_id = ca_rec[0]['address']
                    address_rec = Addresses.objects.get(id = address_id)
                    address_serializers = AddressSerializer(address_rec, data=address_data, context={'request': request})
                    if address_serializers.is_valid(raise_exception=True):
                        address_serializers.save()
                else:
                    address_serializers = AddressSerializer(data=address_data, context={'request': request})
                    if address_serializers.is_valid(raise_exception=True):
                        address_serializers.save()
                        
                        # Create Relation between Customer and Address
                        AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
            returnData = CustomerSerializer(CustomerInstance, context={'request': request})
            return Response(utils.success_msg(returnData.data))
        except Exception as e:
            return Response(utils.error(str(e)))
        
    # Related List 
    @action(detail=True, methods=['get'], url_path = "addresses")
    def get_addresses(self, request, pk=None): 
        queryset = CustomerAddress.objects.filter(customer = pk)
        address_ids = []
        for ele in queryset:
            address_ids.append(ele.address.id)
        address_queryset = Addresses.objects.filter(id__in = address_ids)  
        serializer = AddressSerializer(address_queryset, many = True)         
        return Response(serializer.data)

    # Create Customer Records in Bulk.
    @action(detail=False, methods=['post'], url_path = "import")
    def import_customers(self, request):
        file = request.FILES.get('file')
        sequences = json.loads(request.data.get('sequences'))
        
        count=0
        data_dict = {}

        if file:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2):
                row_data = []
                for cell in row:
                    row_data.append(cell.value)
                for key in sequences:
                    data_dict[key] = row_data[sequences[key]-1]
                try:
                    customer_name = data_dict['customer']
                    if customer_name:
                        if 'shipping_terms' in data_dict:
                            sterm=data_dict['shipping_terms']
                            sterm=utils.encode_api_name(sterm)
                            sp_term = Choice.objects.filter(selector__system_name='shipping_terms', system_name=sterm)
                            if sp_term: data_dict['shipping_terms'] = sp_term.values()[0]['id']
                        
                        if 'ship_via' in data_dict:
                            smethod = data_dict['ship_via']
                            smethod = utils.encode_api_name(smethod)
                            sp_method = Choice.objects.filter(selector__system_name='ship_via', system_name=smethod)
                            if sp_method: data_dict['ship_via'] = sp_method.values()[0]['id']

                        if 'payment_terms' in data_dict:
                            pterm = data_dict['payment_terms']
                            pterm = utils.encode_api_name(pterm)
                            pay_terms = Choice.objects.filter(selector__system_name='payment_terms', system_name=pterm)
                            if pay_terms: data_dict['payment_terms'] = pay_terms.values()[0]['id']

                        if 'payment_method' in data_dict:
                            pmethod = data_dict['payment_method']
                            pmethod = utils.encode_api_name(pmethod)
                            pay_method = Choice.objects.filter(selector__system_name='payment_method', system_name=pmethod)
                            if pay_method: data_dict['payment_method'] = pay_method.values()[0]['id']

                        if 'customer_source' in data_dict:
                            source = data_dict['customer_source']
                            source = utils.encode_api_name(source)
                            cust_source = Choice.objects.filter(selector__system_name='customer_source', system_name=source)
                            if cust_source: data_dict['customer_source'] = cust_source.values()[0]['id']

                        if 'entity' in data_dict:
                            entity = data_dict['entity']
                            entity = utils.encode_api_name(entity)
                            entity = Choice.objects.filter(selector__system_name='entity', system_name=entity)
                            if entity: data_dict['entity'] = entity.values()[0]['id']

                        if 'currency' in data_dict:
                            currency = Currency.objects.filter(code=data_dict['currency'])
                            if currency: data_dict['currency'] = currency.values()[0]['id']       
                        
                        if 'stage' in data_dict:
                            stage_id = Stage.objects.filter(system_name=data_dict['stage'])
                            if stage_id:
                                stage = FormStage.objects.filter(form__system_name='Customer', stage=stage_id.values()[0]['id'])
                                if stage: data_dict['stage'] = stage.values()[0]['stage_id']

                        if 'status' in data_dict:
                            status = data_dict['status']
                            status = utils.encode_api_name(status)
                            status_id = Choice.objects.filter(selector__system_name='status', system_name=status)
                            if status_id: data_dict['status'] = status_id.values()[0]['id']

                        data_dict['require_pos'] = True
                        data_dict['average_pay_days'] = 10
                        data_dict['created_by']=request.user.id
                        
                        serializers = CustomerSerializer(data = data_dict, context={'request': request})
                        if serializers.is_valid(raise_exception=True):
                            serializers.save()
                            count += 1
                except Exception as e:
                    print("Error > ", str(e), data_dict)
                    pass
        else:
            msg="Please Upload A Suitable Excel File."
            return Response(utils.error(msg))
        return Response(utils.success(count))
    
    @action(detail=False, methods=['get'], url_path = "search")
    def search_result(self, request):
        default_filter = ListFilters.objects.filter(list__system_name='Customers', default=True).order_by('sequence')
        query = "Customers.objects.filter("
        filter_list = []

        for filters in default_filter: 
            filter_dict = {}
            logic = filters.logic
            if logic: logic = filters.logic.system_name   
            filter_dict['logic']=logic
            filter_dict['column']=filters.data.field
            filter_dict['field_type']=filters.data.field_type.system_name
            operator = filters.operator
            if operator: operator = filters.operator.system_name    
            filter_dict['operator']=operator
            filter_dict['value']=filters.value
            sublogic = filters.sublogic
            if sublogic: sublogic = filters.sublogic.system_name
            filter_dict['sublogic']=sublogic
            filter_list.append(filter_dict)

        for i in range(len(filter_list)):
            op = filter_list[i]['operator']
            field = filter_list[i]['column']
            field_type = filter_list[i]['field_type']
            value = filter_list[i]['value']
            sublogic = filter_list[i]['sublogic']

            if op == 'is' or op == 'is_not':
                if field_type == 'dropdown': lookup = "%s__system_name__icontains" % field
                if field_type == 'text': lookup = "%s__icontains" % field
                if field_type == 'number': lookup = "%s" % field
            if op == 'is_greater' and field_type == 'number': lookup = "%s__gt" % field
            if op == 'is_less' and field_type == 'number': lookup = "%s__lt" % field
            if op == 'is_greaterthan_or_equal' and field_type == 'number': lookup = "%s__gte" % field
            if op == 'is_lessthan_or_equal' and field_type == 'number': lookup = "%s__lte" % field

            if filter_list[i] == filter_list[-1]:
                new_query = "Q("+lookup+"='"+value+"')"
                if new_query in query:
                    sq = check_parenthesis(self, query)
                    if sq:
                        for i in range(len(sq)):
                            subquery = query+')'
                else: 
                    if op == 'is_not': subquery = query+"~Q("+lookup+"='"+value+"'))"
                    else: subquery = query+"Q("+lookup+"='"+value+"'))"
            else:
                if sublogic:
                    op1 = filter_list[i+1]['operator']
                    field1 = filter_list[i+1]['column']
                    value1 = filter_list[i+1]['value']
                    ft1 = filter_list[i+1]['field_type']

                    if op == 'is_not': sub1 = "~Q("+lookup+"='"+value+"')"
                    else: sub1 = "Q("+lookup+"='"+value+"')"

                    if op1 == 'is' or op1 == 'is_not':
                        if ft1 == 'dropdown': lookup1 = "%s__system_name__icontains" % field1
                        if ft1 == 'text': lookup1 = "%s__icontains" % field1
                        if ft1 == 'number': lookup1 = field1

                    if op1 == 'is_greater' and ft1 == 'number': lookup1 = "%s__gt" % field1
                    if op1 == 'is_less' and ft1 == 'number': lookup1 = "%s__lt" % field1
                    if op1 == 'is_greaterthan_or_equal' and ft1 == 'number': lookup1 = "%s__gte" % field1
                    if op1 == 'is_lessthan_or_equal' and ft1 == 'number': lookup1 = "%s__lte" % field1

                    if op1 == 'is_not': sub2 = "~Q("+lookup1+"='"+value1+"')"
                    else: sub2 = "Q("+lookup1+"='"+value1+"')"

                    if sublogic =='and': subquery = query+"("+sub1+","+sub2+")"
                    elif sublogic == 'or': subquery = query+"("+sub1+"|"+sub2+")"
                else:    
                    if op == 'is_not': subquery = query+"~Q("+lookup+"='"+value+"')"
                    else: subquery = query+"Q("+lookup+"='"+value+"')"

                logic = filter_list[i+1]['logic']
                if logic == 'and': subquery = subquery + ","
                elif logic == 'or': subquery = subquery + "|"
                else: print("Logic >", logic)
            query = subquery
        print(query)
        result = eval(query)
        if result: 
            result = CustomerSerializer(result, many=True, context={'request': request})
            result = result.data
        return Response(utils.success_msg(result))