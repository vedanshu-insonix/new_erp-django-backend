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
            
            returnData = AddressSerializer(AddressInstance)
            return Response(returnData)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
    def update(self, request, pk=None):
        data = request.data
        try:
            address_obj = Address.objects.get(id = pk)
            address_id = address_obj.id
            state_instance = State.objects.get(id = data['state']) if 'state' in data else address_obj.state
            country_instance = Country.objects.get(id = data['country']) if 'country' in data else address_obj.country
            language_instance = Language.objects.get(id = data['language']) if 'language' in data else address_obj.language
            stage_instance = Stage.objects.get(id = data['stage']) if 'stage' in data else address_obj.stage           
            update_record = Address.objects.filter(id = address_id).update(type = data['type'] if 'type' in data else address_obj.type,
                                                                           location = data['location'] if 'location' in data else address_obj.location,
                                                                           first_name = data['first_name'] if 'first_name' in data else address_obj.first_name,
                                                                           last_name = data['last_name'] if 'last_name' in data else address_obj.last_name,
                                                                           company_name = data['company_name'] if 'company_name' in data else address_obj.company_name, 
                                                                           address1 = data['address1'] if 'address1' in data else address_obj.address1, 
                                                                           address2 = data['address2'] if 'address2' in data else address_obj.address2, 
                                                                           address3 = data['address3'] if 'address3' in data else address_obj.address3, 
                                                                           city = data['city'] if 'city' in data else address_obj.city,
                                                                           state =  state_instance,
                                                                           country = country_instance,
                                                                           postal_code = data['postal_code'] if 'postal_code' in data else address_obj.postal_code, 
                                                                           description = data['description'] if 'description' in data else address_obj.description, 
                                                                           comment = data['comment'] if 'comment' in data else address_obj.comment, 
                                                                           warning = data['warning'] if 'warning' in data else address_obj.warning, 
                                                                           icon = data['icon'] if 'icon' in data else address_obj.icon,
                                                                           email = data['email'] if 'email' in data else address_obj.email, 
                                                                           telephone = data['telephone'] if 'telephone' in data else address_obj.telephone, 
                                                                           telephone_type = data['telephone_type'] if 'telephone_type' in data else address_obj.telephone_type,
                                                                           other_communication = data['other_communication'] if 'other_communication' in data else address_obj.other_communication,
                                                                           other_communication_type = data['other_communication_type'] if 'other_communication_type' in data else address_obj.other_communication_type,
                                                                           website = data['website'] if 'website' in data else address_obj.website,
                                                                           stage = stage_instance,
                                                                           stage_started = data['stage_started'] if 'stage_started' in data else address_obj.stage_started,
                                                                           status = data['status'] if 'status' in data else address_obj.status,
                                                                           used = data['used'] if 'used' in data else address_obj.used,
                                                                           language = language_instance
                                                                           )
            # Create Record in CustomerAddress
            customer_instance = Customer.objects.get(id = data['customer']) if 'customer' in data else None
            if customer_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_customer = CustomerAddress.objects.get(address = address_instance.id, customer = customer_instance.id)
                if get_customer:
                    del_obj = get_customer.delete( )
                    CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
            else:
                CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
            
            
            # Create Record in VendorAddress
            vendor_instance = Vendor.objects.get(id = data['vendor']) if 'vendor' in data else None
            if vendor_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_vendor = VendorAddress.objects.get(address = address_instance.id, vendor = vendor_instance.id)
                if get_vendor:
                    del_obj = get_vendor.delete()
                    VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
            else:
                VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
                
            # Create Record in CompanyAddress
            company_instance = Company.objects.get(id = data['company']) if 'company' in data else None
            if company_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_company = CompanyAddress.objects.get(address = address_instance.id, company = company_instance.id)
                if get_company:
                    del_obj = get_company.delete()
                    CompanyAddress.objects.create(address = address_instance, company = company_instance)
            else:
                CompanyAddress.objects.create(address = address_instance, company = company_instance)
                
            # Create Record in CommunicationAddress
            communication_instance = Communication.objects.get(id = data['communication']) if 'communication' in data else None
            if communication_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_commm = CommunicationAddress.objects.get(address = address_instance.id, communication = communication_instance.id)
                if get_commm:
                    del_obj = get_commm.delete()
                    CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)
            else:
                CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)
            serializers = AddressSerializer(address_obj)
            return Response(serializers.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
    def partial_update(self, request, pk=None):
        data = request.data
        try:
            address_obj = Address.objects.get(id = pk)
            address_id = address_obj.id
            state_instance = State.objects.get(id = data['state']) if 'state' in data else address_obj.state
            country_instance = Country.objects.get(id = data['country']) if 'country' in data else address_obj.country
            language_instance = Language.objects.get(id = data['language']) if 'language' in data else address_obj.language
            stage_instance = Stage.objects.get(id = data['stage']) if 'stage' in data else address_obj.stage           
            update_record = Address.objects.filter(id = address_id).update(type = data['type'] if 'type' in data else address_obj.type,
                                                                           location = data['location'] if 'location' in data else address_obj.location,
                                                                           first_name = data['first_name'] if 'first_name' in data else address_obj.first_name,
                                                                           last_name = data['last_name'] if 'last_name' in data else address_obj.last_name,
                                                                           company_name = data['company_name'] if 'company_name' in data else address_obj.company_name, 
                                                                           address1 = data['address1'] if 'address1' in data else address_obj.address1, 
                                                                           address2 = data['address2'] if 'address2' in data else address_obj.address2, 
                                                                           address3 = data['address3'] if 'address3' in data else address_obj.address3, 
                                                                           city = data['city'] if 'city' in data else address_obj.city,
                                                                           state =  state_instance,
                                                                           country = country_instance,
                                                                           postal_code = data['postal_code'] if 'postal_code' in data else address_obj.postal_code, 
                                                                           description = data['description'] if 'description' in data else address_obj.description, 
                                                                           comment = data['comment'] if 'comment' in data else address_obj.comment, 
                                                                           warning = data['warning'] if 'warning' in data else address_obj.warning, 
                                                                           icon = data['icon'] if 'icon' in data else address_obj.icon,
                                                                           email = data['email'] if 'email' in data else address_obj.email, 
                                                                           telephone = data['telephone'] if 'telephone' in data else address_obj.telephone, 
                                                                           telephone_type = data['telephone_type'] if 'telephone_type' in data else address_obj.telephone_type,
                                                                           other_communication = data['other_communication'] if 'other_communication' in data else address_obj.other_communication,
                                                                           other_communication_type = data['other_communication_type'] if 'other_communication_type' in data else address_obj.other_communication_type,
                                                                           website = data['website'] if 'website' in data else address_obj.website,
                                                                           stage = stage_instance,
                                                                           stage_started = data['stage_started'] if 'stage_started' in data else address_obj.stage_started,
                                                                           status = data['status'] if 'status' in data else address_obj.status,
                                                                           used = data['used'] if 'used' in data else address_obj.used,
                                                                           language = language_instance
                                                                           )
            # Create Record in CustomerAddress
            customer_instance = Customer.objects.get(id = data['customer']) if 'customer' in data else None
            if customer_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_customer = CustomerAddress.objects.get(address = address_instance.id, customer = customer_instance.id)
                if get_customer:
                    del_obj = get_customer.delete()
                    CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
            else:
                CustomerAddress.objects.create(address = address_instance, customer = customer_instance)
            
            
            # Create Record in VendorAddress
            vendor_instance = Vendor.objects.get(id = data['vendor']) if 'vendor' in data else None
            if vendor_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_vendor = VendorAddress.objects.get(address = address_instance.id, vendor = vendor_instance.id)
                if get_vendor:
                    del_obj = get_vendor.delete()
                    VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
            else:
                VendorAddress.objects.create(address = address_instance, vendor = vendor_instance)
                
            # Create Record in CompanyAddress
            company_instance = Company.objects.get(id = data['company']) if 'company' in data else None
            if company_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_company = CompanyAddress.objects.get(address = address_instance.id, company = company_instance.id)
                if get_company:
                    del_obj = get_company.delete()
                    CompanyAddress.objects.create(address = address_instance, company = company_instance)
            else:
                CompanyAddress.objects.create(address = address_instance, company = company_instance)
                
            # Create Record in CommunicationAddress
            communication_instance = Communication.objects.get(id = data['communication']) if 'communication' in data else None
            if communication_instance != None:
                address_instance = Address.objects.get(id = address_id)
                get_commm = CommunicationAddress.objects.get(address = address_instance.id, communication = communication_instance.id)
                if get_commm:
                    del_obj = get_commm.delete()
                    CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)
            else:
                CommunicationAddress.objects.create(address = address_instance, communication = communication_instance)

            serializers = AddressSerializer(address_obj)
            return Response(serializers.data)
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