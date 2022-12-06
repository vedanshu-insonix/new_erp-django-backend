from rest_framework import serializers
from ..models.customers import Customers, CustomerAddress
from ..models.address import Addresses
from system.serializers.common_serializers import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from django.db.models import Q

class RelatedCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        exclude = ("created_time","modified_time","created_by")

class RelatedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        exclude = ("created_time","modified_time","created_by")

class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    other_address = serializers.SerializerMethodField()
    
    def get_address(self,obj):
        queryset = CustomerAddress.objects.filter(customer = obj.id)
        address_ids = []
        for ele in queryset:
            address_ids.append(ele.address.id)
        address_queryset = Addresses.objects.filter(Q(id__in = address_ids), Q(address_type = "customer") | Q(address_type = "Customer"))
        serializer = RelatedAddressSerializer(address_queryset, many = True)         
        return serializer.data[0] if serializer.data else None
    
    def get_other_address(self, obj):
        queryset = CustomerAddress.objects.filter(customer = obj.id)
        address_ids = []
        for ele in queryset:
            address_ids.append(ele.address.id)
        address_queryset = Addresses.objects.filter(id__in = address_ids).exclude(Q(address_type = "customer") | Q(address_type = "Customer"),
                                                                                default = True)  
        serializer = RelatedAddressSerializer(address_queryset, many = True)         
        return serializer.data
    
    class Meta:
        model = Customers 
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time", "created_by")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        currency_data = RelatedCurrencySerializer(instance.currency).data
        if 'id' in currency_data:
            response['currency'] = RelatedCurrencySerializer(instance.currency).data
            
        stage_data = RelatedStageSerializer(instance.customer_stage, context={'request': request}).data
        if 'id' in stage_data:
            response['customer_stage'] = RelatedStageSerializer(instance.customer_stage, context={'request': request}).data
            
        created_data = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_data:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        parent_data = RelatedCustomerSerializer(instance.parent_id).data
        if 'id' in parent_data:
            response['parent_id'] = RelatedCustomerSerializer(instance.parent_id).data
        return response
  
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ("address","id","created_time","modified_time","created_by")
        depth = 1