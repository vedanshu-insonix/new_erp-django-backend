from rest_framework import viewsets
from ..serializers.entity_serializers import *
from ..models.entity import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from system import utils
from system.models.teams import Team
from sales.serializers.addresses_serializers import AddressSerializer, Choice


class EntityViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Company to be modified.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            GetData = request.data
            company_fields = [f.name for f in Entity._meta.get_fields()]
            address_fields = [f.name for f in Addresses._meta.get_fields()]
            company_data = {}
            address_data = {}
            
            for keys, values in GetData.items():
                if keys in company_fields:
                    company_data[keys] = values
                elif keys in address_fields:
                    address_data[keys] = values
            if company_data:
                serializer=EntitySerializer(data=company_data, context={'request':request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                entityId = serializer.data.get('id')
                if address_data:
                    address_data['company'] = entityId
                    newAddr = AddressSerializer(data=address_data, context={'request':request})
                    if newAddr.is_valid(raise_exception=True):
                        newAddr.save()   
            companyRec=Entity.objects.get(id=entityId)
            result=EntitySerializer(companyRec, context={'request':request})
            return Response(utils.success_msg(result.data))
        except Exception as e:
            return Response(utils.error(str(e)))
        
    def update(self, request, pk=None):
        relId = None
        try:
            GetData = request.data
            entityRec = Entity.objects.get(id=pk)
            company_fields = [f.name for f in Entity._meta.get_fields()]
            address_fields = [f.name for f in Addresses._meta.get_fields()]
            company_data = {}
            address_data = {}
            
            for keys, values in GetData.items():
                if keys in company_fields:
                    company_data[keys] = values
                elif keys in address_fields:
                    address_data[keys] = values
            if address_data:
                addrRec = Addresses.objects.filter(company = pk)
                if addrRec:
                    addrrec=Addresses.objects.get(company = pk)
                    oldType = addrRec.address_type
                    newType = address_data['address_type']
                    if oldType == newType:
                        address_serializers = AddressSerializer(addrrec, data=address_data, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                            address_serializers.save()
                    else:
                        address_data['company']=entityRec.id
                        address_serializers = AddressSerializer(data=address_data, context={'request': request})
                        if address_serializers.is_valid(raise_exception=True):
                            address_serializers.save()
                else:
                    address_data['company']=entityRec.id
                    address_serializers = AddressSerializer(data=address_data, context={'request': request})
                    if address_serializers.is_valid(raise_exception=True):
                        address_serializers.save()
            if company_data:
                serializers = EntitySerializer(entityRec, data = company_data, context={'request': request})
                if serializers.is_valid(raise_exception=True):
                    serializers.save()
            returnData = EntitySerializer(entityRec, context={'request': request})
            return Response(utils.success_msg(returnData.data))
        except Exception as e:
            return Response(utils.error(str(e)))