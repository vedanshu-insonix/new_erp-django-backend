from django.shortcuts import render
from rest_framework import viewsets
from system.models.common import *
from ..models.customers import Customer, CustomerAddress
from ..serializers.addresses_serializers import AddressSerializer, AddressTagSerializer
from ..models.address import Address
from system.models.communication import Communication, CommunicationAddress
from ..models.vendors import Vendor, VendorAddress
from system.models.company import Company, CompanyAddress
from ..models.address import AddressTag
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import filters

 
class AddressViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Addresses to be modified.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
    def create(self, request, *args, **kwargs):
        GetData = request.data
        HaveCustomer = False
        HaveVendor = False
        HaveCompany = False
        HaveCommunication = False
        try: 
            
            #************* Separating Customer *****************
            if 'customer' in GetData:
                customer = GetData.pop("customer")
                HaveCustomer = True
            
            #************* Separating Vendor ********************
            if 'vendor' in GetData:
                vendor = GetData.pop("vendor")
                HaveVendor = True
            
            #************* Separating Company ********************
            if 'company' in GetData:
                company = GetData.pop("company")
                HaveCompany = True
            
            #************* Separa ting Communication **************
            if 'communication' in GetData:
                communication = GetData.pop("communication")
                HaveCommunication = True
            
            #************ Create Address **************************
            serializers = AddressSerializer(data = GetData, context={'request': request})
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                AddressInstance = Address.objects.get(id = serializers.data.get("id"))
                
                if HaveCustomer == True:
                    CustomerInstance = Customer.objects.get(id = customer)
                    if CustomerInstance:
                        CustomerAddress.objects.create(address = AddressInstance, customer = CustomerInstance)
                
                if HaveVendor == True:
                    VendorInstance = Vendor.objects.get(id = vendor)
                    if VendorInstance:
                        VendorAddress.objects.create(address = AddressInstance, vendor = VendorInstance)

                if HaveCompany == True:
                    CompanyInstance = Company.objects.get(id = company)
                    if CompanyInstance:
                        CompanyAddress.objects.create(address = AddressInstance, company = CompanyInstance)

                if HaveCommunication == True:
                    CommunicationInstance = Communication.objects.get(id = communication) 
                    if CommunicationInstance:
                        CommunicationAddress.objects.create(address = AddressInstance, communication = CommunicationInstance)
            
            returnData = AddressSerializer(AddressInstance, context={'request': request})
            return Response(returnData.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
    def update(self, request, pk=None):
        data = request.data
        HaveCustomer = False
        HaveVendor = False
        HaveCompany = False
        HaveCommunication = False
        try:
             #************* Separating Customer *****************
            if 'customer' in data:
                customer = data.pop("customer")
                HaveCustomer = True
            
            #************* Separating Vendor ********************
            if 'vendor' in data:
                vendor = data.pop("vendor")
                HaveVendor = True
            
            #************* Separating Company ********************
            if 'company' in data:
                company = data.pop("company")
                HaveCompany = True
            
            #************* Separa ting Communication **************
            if 'communication' in data:
                communication = data.pop("communication")
                HaveCommunication = True

            address_obj = Address.objects.get(id = pk)
            serializer = AddressSerializer(address_obj, data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            address_id = address_obj.id
            
            # Create Record in CustomerAddress
            if HaveCustomer==True:
                customer_instance = Customer.objects.get(id = customer)
                address_instance = Address.objects.get(id = address_id)
                if customer_instance != None:
                    get_customer = CustomerAddress.objects.filter(address = address_instance.id, customer = customer_instance.id)
                    if get_customer:
                        del_obj = get_customer.delete( )
                        CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
                    else:
                        CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
            
            # Create Record in VendorAddress
            if HaveVendor == True:
                vendor_instance = Vendor.objects.get(id = vendor)
                if vendor_instance != None:
                    address_instance = Address.objects.get(id = address_id)
                    get_vendor = VendorAddress.objects.filter(address = address_instance.id, vendor = vendor_instance.id)
                    if get_vendor:
                        del_obj = get_vendor.delete()
                        VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
                    else:
                        VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
                
            # Create Record in CompanyAddress
            if HaveCompany == True:
                company_instance = Company.objects.get(id = company)
                if company_instance != None:
                    address_instance = Address.objects.get(id = address_id)
                    get_company = CompanyAddress.objects.filter(address = address_instance.id, company = company_instance.id)
                    if get_company:
                        del_obj = get_company.delete()
                        CompanyAddress.objects.create(address = address_instance, company = company_instance)
                    else:
                        CompanyAddress.objects.create(address = address_instance, company = company_instance)

            # Need to do some modification to also update same data in communication table through address api call    
            # Create Record in CommunicationAddress
            """if HaveCommunication == True:
                communication_instance = Communication.objects.get(id = communication)
                if communication_instance != None:
                    address_instance = Address.objects.get(id = address_id)
                    get_commm = CommunicationAddress.objects.filter(address = address_instance.id, communication = communication_instance.id)
                    if get_commm:
                        del_obj = get_commm.delete()
                        CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)
                    else:
                        CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)"""
            serializer = AddressSerializer(address_obj)
            return Response(serializer.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    

    # To add tags on addresses
    @action(detail=False, methods=['post'],url_path = "addtags")
    def addtags(self, request):
        try:
            result = []
            tag = request.data.get('tags')
            address_ids = request.data.get('address_ids')
            for i in range(len(tag)):
                try:
                    tag_data = Tag.objects.get(name=tag[i].get('name'))
                except:
                    tag_data = None
                    pass
                if tag_data:
                    pass
                else:
                    tag_data = Tag.objects.create(name=tag[i].get('name'),color=tag[i].get('color'),created_by_id = request.user.id)
                response = AddressTag.objects.create(tag_id=tag_data.id,address_id=address_ids[i],created_by_id = request.user.id)
                result.append(response)
            serializer = AddressTagSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            raise Http404()

    # to remove tags from address
    @action(detail=False, methods=['post'],url_path = "removetags")
    def removetags(self,request):
        try:
            tag = request.data.get('tags')
            address_ids = request.data.get('address_ids')
            for i in range(len(tag)):
                try:
                    tag_data = Tag.objects.get(name=tag[i].get('name'))
                except:
                    tag_data = None
                    pass
                if tag_data:
                    AddressTag.objects.filter(address_id=address_ids[i],tag_id=tag_data.id).delete()
            return Response({'status': 'success','code': status.HTTP_200_OK})
        except Exception as e:
            print(str(e))
            raise Http404()