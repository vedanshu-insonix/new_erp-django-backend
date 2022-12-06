from rest_framework import serializers
from system.serializers.common_serializers import *
from ..models.vendors import Vendors, VendorAddress, VendorProducts
from system.serializers.user_serializers import RelatedUserSerilaizer


class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        exclude = ("address","id")
        depth = 1
    
class RelatedVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        exclude = ("created_time","modified_time","created_by")
        
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        purchase_currency_data = RelatedCurrencySerializer(instance.purchasing_currency).data
        if 'id' in purchase_currency_data:
            response['purchasing_currency'] = RelatedCurrencySerializer(instance.purchasing_currency).data
            
        stage_data = RelatedStageSerializer(instance.stage).data
        if 'id' in stage_data:
            response['stage'] = RelatedStageSerializer(instance.stage).data
            
        created_data = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_data:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        parent_data = RelatedVendorSerializer(instance.parent_id).data
        if 'id' in parent_data:
            response['parent_id'] = RelatedVendorSerializer(instance.parent_id).data
        return response

class VendorProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProducts
        fields = ('__all__')