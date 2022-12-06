from ast import Add
import json
from django.shortcuts import render
from rest_framework import viewsets
from system import utils
from ..models.customers import Customers, CustomerAddress
from ..models.address import Addresses
from ..serializers.customers_serializers import CustomerSerializer, RelatedAddressSerializer
from ..serializers.addresses_serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters
import openpyxl
from system.utils import *

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("__all__")
    filterset_fields = {
            'customer': ['exact', 'contains'],'entity': ['exact', 'contains'],'shipping_terms': ['exact', 'contains'],
            'ship_via': ['exact', 'contains'],'customer_source': ['exact', 'contains'],'payment_terms': ['exact', 'contains'],'payment_method': ['exact', 'contains'],
            'currency' : ['exact'],'free_freight_minimum' : ['exact', 'contains'],'issue_statements' : ['exact'],
            'require_pos': ['exact'],'credit_limit': ['exact', 'contains'],'account_balance': ['exact', 'contains'],
            'current_orders': ['exact', 'contains'], 'authorised_card': ['exact', 'contains'], 'credit_available': ['exact', 'contains'],
            'overdue': ['exact'],'average_pay_days': ['exact'],'last_credit_review': ['exact'],'credit_hold': ['exact'],
            'customer_receivable_account': ['exact'],'customer_stage': ['exact'],'stage_started': ['exact'],'status': ['exact'], 'used': ['exact']
        }
    ordering_fields = ("__all__")
        
    def create(self, request, *args, **kwargs):
        GetData = request.data
        HaveAddr = False
        HaveDefAdd = False
        try:
            #************* separating default address ************ 
            if 'address' in GetData:
                address = GetData.pop("address")
                address['default'] = True
                HaveDefAdd = True

            #************ separating Other address **************
            if 'other_address' in GetData:
                OtherAddress = GetData.pop("other_address")
                HaveAddr = True
            
            #************ Create Customer ***********************
            serializers = CustomerSerializer(data = GetData, context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                # customerId = serializers.data.get("id")
                CustomerInstance = Customers.objects.get(id = serializers.data.get("id"))
                #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__address_type = "customer") | Q(address__address_type = "Customer"),
                                                                        Q(address__default = True)).first()
                    if GetCustomerAddress:
                        AddressInstance = Addresses.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(AddressInstance,data=address, context={'request': request})
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                
                #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    for address in OtherAddress:
                        if "id" in address:
                            addressInstance = Addresses.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                            CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
            returnData = CustomerSerializer(CustomerInstance, context={'request': request})
            return Response(returnData.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
        
    def update(self, request, pk=None):
        GetData = request.data
        HaveAddr = False
        HaveDefAdd = False
        try:
            #************* separating default address ************ 
            if 'address' in GetData:
                address = GetData.pop("address")
                HaveDefAdd = True

            #************ separating Other address **************
            if 'other_address' in GetData:
                OtherAddress = GetData.pop("other_address")
                HaveAddr = True

            #************ Update Customer ******************
            CustomerInstance = Customers.objects.get(id=pk)
            serializers = CustomerSerializer(CustomerInstance, data=GetData,  context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                print(HaveAddr)
            #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__address_type = "customer") | Q(address__address_type = "Customer"),
                                                                        Q(address__default = True)).first()
                    
                    if GetCustomerAddress:
                        AddressInstance = Addresses.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(AddressInstance,data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                print(address_serializers.data)
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
    
            
            #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    
                    for address in OtherAddress:
                        
                        if 'id' in OtherAddress:
                            addressInstance = Addresses.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                            CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
            return Response(serializers.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
    def partial_update(self, request, pk=None):
        GetData = request.data
        HaveAddr = False
        HaveDefAdd = False
        try:
            #************* separating default address ************ 
            if 'address' in GetData:
                address = GetData.pop("address")
                HaveDefAdd = True

            #************ separating Other address **************
            if 'other_address' in GetData:
                OtherAddress = GetData.pop("other_address")
                HaveAddr = True

            #************ Update Customer ******************
            CustomerInstance = Customers.objects.get(id=pk)
            serializers = CustomerSerializer(CustomerInstance, data=GetData,  context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                
            #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__address_type = "customer") | Q(address__address_type = "Customer"),
                                                                        Q(address__default = True)).first()
                    if GetCustomerAddress:
                        AddressInstance = Addresses.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(GetCustomerAddress,data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                        
            #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    for address in OtherAddress:
                        if 'id' in OtherAddress:
                            addressInstance = Addresses.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Addresses.objects.get(id = address_serializers.data.get("id"))
                            CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
            return Response(serializers.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
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

    @action(detail=False, methods=['post'], url_path = "import")
    def import_customers(self, request):
        try:
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
                    if 'Customer' in row_data:
                        pass
                    else:
                        for key in sequences:
                            data_dict[key] = row_data[sequences[key]-1]
                        data_dict['entity'] = '1'
                        data_dict['require_pos'] = True
                        data_dict['average_pay_days'] = 10
                        data_dict['last_credit_review'] = '2022-12-11'
                        data_dict['used'] = '2022-12-11'
                        data_dict['created_by']=request.user.id
                        # sorting data based on the sequence from the front-end
                       
                        serializers = CustomerSerializer(data = data_dict, context={'request': request})
                        if serializers.is_valid(raise_exception=True):
                            serializers.save()
                            count += 1
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
            return Response(utils.success(self,count))
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
    



