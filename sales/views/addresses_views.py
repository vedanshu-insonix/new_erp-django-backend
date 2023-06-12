from django.shortcuts import render
from rest_framework import viewsets
from system.models.common import *
from ..models.customers import Customers
from ..serializers.addresses_serializers import AddressSerializer, RelatedAddressSerializer
from system.serializers.communication_serializers import CommunicationSerializer
from ..models.address import Addresses
from system.models.communication import Communication
from ..models.vendors import Vendors
from system.models.entity import Entity
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.signals import post_save
from django.dispatch import receiver
from system.service import get_rid_pkey
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import filters
from system import utils
import openpyxl
import json
 
class AddressViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Addresses to be modified.
    """
    queryset = Addresses.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
            'address_type__system_name': ['exact', 'icontains'],'address_location_type__system_name': ['exact', 'icontains'],'first_name': ['icontains'],
            'last_name': ['icontains'],'company_name': ['exact', 'icontains'],'city': ['exact', 'icontains'],'state__system_name': ['exact', 'icontains'],
            'postal_code' : ['exact'],'country__system_name' : ['exact', 'icontains'],'email' : ['exact']
            }
    #filterset_fields = ("__all__")
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
            
            #************* Separating Communication **************
            if 'communication' in GetData:
                communication = GetData.pop("communication")
                HaveCommunication = True
            
            #************ Create Address **************************
            serializer = AddressSerializer(data = GetData, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                AddressInstance = Addresses.objects.get(id = serializer.data.get("id"))
                if HaveCustomer == True:
                    CustomerInstance = Customers.objects.get(id = customer)
                    if CustomerInstance:
                        CustomerInstance.address.add(AddressInstance.id)
                        #CustomerInstance.objects.create(address = AddressInstance, customer = CustomerInstance)
                
                if HaveVendor == True:
                    VendorInstance = Vendors.objects.get(id = vendor)
                    if VendorInstance:
                        VendorInstance.address.add(AddressInstance.id)
                        #VendorAddress.objects.create(address = AddressInstance, vendor = VendorInstance)

                if HaveCompany == True:
                    CompanyInstance = Entity.objects.get(id = company)
                    if CompanyInstance:
                        CompanyInstance.address.add(AddressInstance.id)
                    #     EntityAddress.objects.create(address = AddressInstance, company = CompanyInstance)
                if HaveCommunication == True:
                    for comm in communication:
                        if "id" in comm:
                            CommunicationInstance = Communication.objects.get(id= comm.pop("id"))
                            updateCommunication = CommunicationSerializer(CommunicationInstance,data=comm, context={'request': request})
                            if updateCommunication.is_valid(raise_exception=True):
                                updateCommunication.save()
                        else:
                            comm_serializers = CommunicationSerializer(data=comm, context={'request': request})
                            if comm_serializers.is_valid(raise_exception=True):
                                comm_serializers.save()
                            # Create Relation between Communication and Address
                            CommunicationInstance = Communication.objects.get(id = comm_serializers.data.get("id"))
                            AddressInstance.communications.add(CommunicationInstance.id)
                            #CreateCommunicationAddress = CommunicationAddress.objects.create(address = AddressInstance, communication = CommunicationInstance)
            
            returnData = AddressSerializer(AddressInstance, context={'request': request})
            return Response(returnData.data)
        except Exception as e:
            return Response(utils.error(str(e)))
    
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

            address_obj = Addresses.objects.get(id = pk)
            serializer = AddressSerializer(address_obj, data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
            address_id = address_obj.id
            # Create Record in CustomerAddress
            if HaveCustomer == True:
                CustomerInstance = Customers.objects.get(id = customer)
                if CustomerInstance:
                    CustomerInstance.address.add(address_obj.id)
            
            # Create Record in VendorAddress
            if HaveVendor == True:
                VendorInstance = Vendors.objects.get(id = vendor)
                if VendorInstance:
                    VendorInstance.address.add(address_obj.id)
            
            # Create Record in EntityAddress
            if HaveCompany == True:
                CompanyInstance = Entity.objects.get(id = company)
                if CompanyInstance:
                    CompanyInstance.address.add(address_obj.id)
  
            # Create Record in CommunicationAddress
            if HaveCommunication == True:
                for comm in communication:
                    if "id" in comm:
                        CommunicationInstance = Communication.objects.get(id= comm.pop("id"))
                        updateCommunication = CommunicationSerializer(CommunicationInstance,data=comm, context={'request': request})
                        if updateCommunication.is_valid(raise_exception=True):
                                updateCommunication.save()
                    else:  
                        comm_serializers = CommunicationSerializer(data=comm, context={'request': request})
                        if comm_serializers.is_valid(raise_exception=True):
                                comm_serializers.save()
                        CommunicationInstance = Communication.objects.get(id = comm_serializers.data.get("id"))
                        address_obj.communications.add(CommunicationInstance.id)
                        #CreateCommunicationAddress = CommunicationAddress.objects.create(address = address_instance, communication = CommunicationInstance)
                        
            serializer = AddressSerializer(address_obj, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
           return Response(utils.error(str(e)))
    
    
    # To add tags on addresses
    """@action(detail=False, methods=['post'],url_path = "addtags")
    def addtags(self, request):
        try:
            result = []
            tag = request.data.get('tags')
            address_ids = request.data.get('address_ids')
            for i in range(len(tag)):
                tag_data = Tag.objects.filter(tag=tag[i].get('tag'))
                if not tag_data:
                    tag_data = Tag.objects.create(tag=tag[i].get('tag'),color=tag[i].get('color'),created_by_id = request.user.id)
                response = AddressTag.objects.create(tag_id=tag_data.id,address_id=address_ids[i],created_by_id = request.user.id)
                result.append(response)
            serializer = AddressSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(utils.error(self,str(e)))"""

    # to remove tags from address
    """@action(detail=False, methods=['post'],url_path = "removetags")
    def removetags(self,request):
        try:
            tag = request.data.get('tags')
            address_ids = request.data.get('address_ids')
            for i in range(len(tag)):
                tag_data = Tag.objects.filter(tag=tag[i].get('tag'))
                if not tag_data:
                    AddressTag.objects.filter(address_id=address_ids[i],tag_id=tag_data.id).delete()
            return Response({'status': 'success','code': status.HTTP_200_OK})
        except Exception as e:
            return Response(utils.error(self,str(e)))"""

    # Create Address Records in Bulk.    
    @action(detail=False, methods=['post'], url_path = "import")
    def import_address(self, request):
        try:
            file = request.FILES.get('file')
            new_sequence = json.loads(request.data.get('sequence'))
            
            count=0
            data_dict = {}
            defective_data = {}

            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2):
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    for i in range(len(row_data)):
                        if row_data[i] is None:
                            have_data=False
                        else:
                            have_data=True
                            break
                    if have_data==True:
                        if 'address_type' in row_data:
                            defective_data[count+1] = "heading section"
                            pass
                        else:
                            for key in new_sequence:
                                data_dict[key] = row_data[new_sequence[key]-1]
                                if key == 'state':
                                    state_name = row_data[new_sequence[key]-1]
                                    state_name = State.objects.filter(name=state_name)
                                    data_dict[key]=state_name.values()[0]['id']
                                if key == 'country':
                                    country_name = row_data[new_sequence[key]-1]
                                    country_name = Country.objects.filter(name=country_name)
                                    data_dict[key] = country_name.values()[0]['id']
                                if key == 'stage':
                                    stage_name = row_data[new_sequence[key]-1]
                                    stage_name = Stage.objects.filter(stage=stage_name)
                                    data_dict[key] = stage_name.values()[0]['id']
                                if key == 'language':
                                    language = row_data[new_sequence[key]-1]
                                    language = Language.objects.filter(name=language)
                                    data_dict[key]=language.values()[0]['id']
                            try:       
                                serializers = AddressSerializer(data = data_dict, context={'request': request})
                                if serializers.is_valid(raise_exception=True):
                                    serializers.save()
                                    count += 1
                            except Exception as e:
                                defective_data[count+1] = str(e)
                                msg = f"skipped row(s) {defective_data}"
                                pass
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(msg))
            if msg:
                return Response(utils.success_def(count,msg))
            else:
                return Response(utils.success(count))
        except Exception as e:
            return Response(utils.error(str(e)))

# To Update the communication record after the updation of any address record.
@receiver(post_save, sender=Addresses)
def update_comm(created, instance,**kwargs):
    print("demo")
    address_id = instance.id
    email = instance.email
    telephone = instance.telephone
    telephone_type = instance.telephone_type
    addressInstance = Addresses.objects.get(id = address_id)
    get_comm_addr = Communication.objects.filter(address = address_id, primary = True)

    print(get_comm_addr)
    
    if get_comm_addr:
        if email != None:
            for comm_addr in get_comm_addr:
                communication_detail = Communication.objects.filter(id = comm_addr.id).first()
                if communication_detail:
                    communication_channel = communication_detail.communication_channel
                    if communication_channel != None:
                        get_choice = Choice.objects.filter(id = communication_channel).first()
                        if get_choice:
                            choice = get_choice.system_name
                            if choice == 'email' or choice == 'Email':
                                update_comm = Communication.objects.filter(id = communication_detail.id).update(value = email)
                                
        if telephone != None and telephone_type != None:
            for comm_addr in get_comm_addr:
                communication_detail = Communication.objects.filter(id = comm_addr.id).first()
                if communication_detail:
                    communication_channel = communication_detail.communication_channel
                    communication_type = communication_detail.communication_type
                    if communication_channel != None:
                        get_choice = Choice.objects.filter(id = communication_channel).first()
                        type_choice = Choice.objects.filter(id = communication_type).first()
                        if get_choice:
                            choice = get_choice.system_name
                            if choice == 'telephone' or choice == 'Telephone':
                                Communication.objects.filter(id = communication_detail.id).update(value = telephone,
                                                                                                communication_type = type_choice.id)                        
        
        elif telephone != None:
            for comm_addr in get_comm_addr:
                communication_detail = Communication.objects.filter(id = comm_addr.id).first()
                if communication_detail:
                    communication_channel = communication_detail.communication_channel
                    communication_type = communication_detail.communication_type
                    if communication_channel != None:
                        get_choice = Choice.objects.filter(id = communication_channel).first()
                        type_choice = Choice.objects.filter(id = communication_type).first()
                        if get_choice:
                            choice = get_choice.system_name
                            if choice == 'telephone' or choice == 'Telephone':
                                Communication.objects.filter(id = communication_detail.id).update(value = telephone)
                
    else:
        if email != None:
            get_choice = Choice.objects.filter(selector__system_name = "communication_channel", system_name='email').first()
            if get_choice:
                comm_id = get_rid_pkey('communications')
                create_comm = Communication.objects.create(id = comm_id, value = email, communication_channel = get_choice.id, 
                                                           primary = True, address_id=address_id)
                # addressInstance.communications.add(create_comm.id)
                # CommunicationAddress.objects.create(address = address_instance, communication = create_comm)
        
        if telephone != None and telephone_type != None:
            get_choice = Choice.objects.filter(selector__system_name = "communication_channel", system_name='telephone').first()
            type_choice = Choice.objects.filter(id = telephone_type, selector__system_name = "telephone_type").first()
            if get_choice and type_choice:
                comm_id = get_rid_pkey('communications')
                create_comm = Communication.objects.create(id = comm_id, value = telephone,
                                                        communication_channel = get_choice.id,
                                                        communication_type = type_choice.id,
                                                        primary = True, address_id=address_id)
                # addressInstance.communications.add(create_comm.id)
                # CommunicationAddress.objects.create(address = address_instance, communication = create_comm)
            
        elif telephone != None:
            get_choice = Choice.objects.filter(selector__system_name = "communication_channel", system_name='telephone').first()
            if get_choice:
                comm_id = get_rid_pkey('communications')
                create_comm = Communication.objects.create(id = comm_id, value = telephone,
                                                    communication_channel = get_choice.id,
                                                    primary = True, address_id=address_id)
                # addressInstance.communications.add(create_comm.id)
                # CommunicationAddress.objects.create(address = address_instance, communication = create_comm, primary = True)