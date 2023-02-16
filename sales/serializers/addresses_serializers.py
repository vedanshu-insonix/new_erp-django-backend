from rest_framework import serializers
from ..models.address import Addresses, AddressTag
from system.serializers.common_serializers import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.entity_serializers import EntityAddressSerializer
from system.serializers.communication_serializers import CommunicationAddressSerializer
from system.models.entity import EntityAddress
from system.models.communication import Communication
from system.serializers.communication_serializers import RelatedCommunicationSerializer
from system.models.communication import CommunicationAddress
from .customers_serializers import CustomerAddressSerializer
from .vendors_serializers import VendorAddressSerializer
from ..models.customers import CustomerAddress
from ..models.vendors import VendorAddress
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers


class AddressTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressTag
        fields = ("tag",)
        depth = 1
    
class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    entity = serializers.SerializerMethodField()
    communication = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    def get_customer(self, obj):
        queryset = CustomerAddress.objects.filter(address = obj.id)
        serializer = CustomerAddressSerializer(queryset, many=True)
        return_customer = serializer.data[0]['customer'] if serializer.data else None
        return return_customer

    def get_vendor(self, obj):
        queryset = VendorAddress.objects.filter(address = obj.id)
        serializer = VendorAddressSerializer(queryset, many=True)
        return_vendor = serializer.data[0]['vendor'] if serializer.data else None
        return return_vendor

    def get_entity(self, obj):
        queryset = EntityAddress.objects.filter(address = obj.id)
        serializer = EntityAddressSerializer(queryset, many=True)
        return_entity = serializer.data[0]['entity'] if serializer.data else None
        return return_entity

    def get_communication(self, obj):
        queryset = CommunicationAddress.objects.filter(address = obj.id)
        ids = []
        for ele in queryset:
            ids.append(ele.communication.id)
        comm_queryset = Communication.objects.filter(id__in = ids)
        serializer = RelatedCommunicationSerializer(comm_queryset, many=True)
        return serializer.data

    def get_tags(self, obj):
        queryset = AddressTag.objects.filter(address = obj.id)
        ids = []
        for ele in queryset:
            ids.append(ele.tag.id)
        tags_queryset = Tag.objects.filter(id__in = ids)
        serializer = RelatedTagSerializer(tags_queryset, many=True)
        return serializer.data

    class Meta:
        model = Addresses
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        state = RelatedStateSerializer(instance.state, context={'request': request}).data
        if 'id' in state:
            response['state'] = RelatedStateSerializer(instance.state, context={'request': request}).data
            
        country = RelatedCountrySerializer(instance.country, context={'request': request}).data
        if 'id' in country:
            response['country'] = RelatedCountrySerializer(instance.country, context={'request': request}).data
            
        language = RelatedLanguageSerializer(instance.language, context={'request': request}).data
        if 'id' in language:
            response['language'] = RelatedLanguageSerializer(instance.language, context={'request': request}).data

        stage = RelatedStageSerializer(instance.stage, context={'request': request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Addresses')
        if record_id:
            data['id']=get_primary_key('Addresses')
        return data