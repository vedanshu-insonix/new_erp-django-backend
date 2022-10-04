from rest_framework import serializers
from ..models.address import Address, AddressTag
from system.serializers.common_serializers import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.company_serializers import CompanyAddressSerializer
from system.serializers.communication_serializers import CommunicationAddressSerializer
from system.models.company import CompanyAddress
from system.models.communication import CommunicationAddress
from .customers_serializers import CustomerAddressSerializer
from .vendors_serializers import VendorAddressSerializer
from ..models.customers import CustomerAddress
from ..models.vendors import VendorAddress


class AddressTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressTag
        fields = ("tag",)
        depth = 1
    
class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
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

    def get_company(self, obj):
        queryset = CompanyAddress.objects.filter(address = obj.id)
        serializer = CompanyAddressSerializer(queryset, many=True)
        return_company = serializer.data[0]['company'] if serializer.data else None
        return return_company

    def get_communication(self, obj):
        queryset = CommunicationAddress.objects.filter(address = obj.id)
        serializer = CommunicationAddressSerializer(queryset, many=True)
        return_comm = serializer.data[0]['communication'] if serializer.data else None
        return return_comm

    def get_tags(self, obj):
        queryset = AddressTag.objects.filter(address = obj.id)
        ids = []
        for ele in queryset:
            ids.append(ele.tag.id)
        tags_queryset = Tag.objects.filter(id__in = ids)
        serializer = RelatedTagSerializer(tags_queryset, many=True)
        return serializer.data

    class Meta:
        model = Address
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        state = RelatedStateSerializer(instance.state).data
        if 'id' in state:
            response['state'] = RelatedStateSerializer(instance.state).data
            
        country = RelatedCountrySerializer(instance.country).data
        if 'id' in country:
            response['country'] = RelatedCountrySerializer(instance.country).data
            
        language = RelatedLanguageSerializer(instance.language).data
        if 'id' in language:
            response['language'] = RelatedLanguageSerializer(instance.language).data

        stage = RelatedStageSerializer(instance.stage).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage).data
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    
        
        
        