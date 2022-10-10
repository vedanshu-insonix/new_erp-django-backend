from ast import Add
from django.shortcuts import render
from rest_framework import viewsets
from ..models.customers import Customer, CustomerAddress
from ..models.address import Address
from ..serializers.customers_serializers import CustomerSerializer, RelatedAddressSerializer
from ..serializers.addresses_serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import filters

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("__all__")
    filterset_fields = {
            'name': ['exact', 'contains'],'entity': ['exact', 'contains'],'shipping_terms': ['exact', 'contains'],
            'ship_via': ['exact', 'contains'],'source': ['exact', 'contains'],'payment_terms': ['exact', 'contains'],'payment_method': ['exact', 'contains'],
            'sales_currency' : ['exact'],'free_freight_min' : ['exact', 'contains'],'issue_statements' : ['exact'],
            'require_pos': ['exact'],'credit_limit': ['exact', 'contains'],'account_balance': ['exact', 'contains'],
            'current_orders': ['exact', 'contains'], 'authorised_card': ['exact', 'contains'], 'credit_avail': ['exact', 'contains'],
            'overdue': ['exact'],'avg_pay_days': ['exact'],'last_credit_review': ['exact'],'credit_hold': ['exact'],
            'account_receivable': ['exact'],'stage': ['exact'],'stage_started': ['exact'],'status': ['exact'], 'used': ['exact']
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
                CustomerInstance = Customer.objects.get(id = serializers.data.get("id"))
                #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__type = "customer") | Q(address__type = "Customer"),
                                                                        Q(address__default = True)).first()
                    if GetCustomerAddress:
                        AddressInstance = Address.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(AddressInstance,data=address, context={'request': request})
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                
                #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    for address in OtherAddress:
                        if "id" in address:
                            addressInstance = Address.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
                            CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
            returnData = CustomerSerializer(CustomerInstance)
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
            CustomerInstance = Customer.objects.get(id=pk)
            serializers = CustomerSerializer(CustomerInstance, data=GetData,  context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                print(HaveAddr)
            #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__type = "customer") | Q(address__type = "Customer"),
                                                                        Q(address__default = True)).first()
                    
                    if GetCustomerAddress:
                        AddressInstance = Address.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(AddressInstance,data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                print(address_serializers.data)
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
    
            
            #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    
                    for address in OtherAddress:
                        
                        if 'id' in OtherAddress:
                            addressInstance = Address.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
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
            CustomerInstance = Customer.objects.get(id=pk)
            serializers = CustomerSerializer(CustomerInstance, data=GetData,  context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                
            #*************************** Creating/Updating default address ****************************
                if HaveDefAdd == True:
                    GetCustomerAddress = CustomerAddress.objects.filter(Q(customer = CustomerInstance),
                                                                        Q(address__type = "customer") | Q(address__type = "Customer"),
                                                                        Q(address__default = True)).first()
                    if GetCustomerAddress:
                        AddressInstance = Address.objects.get(id = GetCustomerAddress.address.id)
                        address_serializers = AddressSerializer(GetCustomerAddress,data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                    else:
                        address_serializers = AddressSerializer(data=address, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                                address_serializers.save()
                                
                        # Create Relation between Customer and Address
                        AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
                        CreateCustomerAddress = CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                        
            #*************************** Creating/Updating Other Addresses ***************************** 
                if HaveAddr == True:
                    for address in OtherAddress:
                        if 'id' in OtherAddress:
                            addressInstance = Address.objects.get(id= address.pop("id"))
                            updateAddress = AddressSerializer(addressInstance,data=address, context={'request': request})
                            if updateAddress.is_valid(raise_exception=True):
                                    updateAddress.save()
                        else:  
                            address_serializers = AddressSerializer(data=address, context={'request': request})
                            if address_serializers.is_valid(raise_exception=True):
                                    address_serializers.save()
                            # Create Relation between Customer and Address
                            AddressInstance = Address.objects.get(id = address_serializers.data.get("id"))
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
        address_queryset = Address.objects.filter(id__in = address_ids)  
        serializer = AddressSerializer(address_queryset, many = True)         
        return Response(serializer.data)
    
    



