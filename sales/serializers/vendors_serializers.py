from rest_framework import serializers
from system.serializers.common_serializers import *
from ..models.vendors import Vendors, VendorAddress, VendorProducts, VendorPrices
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
    
    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='vendors')
        if record_id:
            data['id']=get_rid_pkey('vendors')
        return data

class VendorProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProducts
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='vendorproducts')
        if record_id:
            data['id']=get_rid_pkey('vendorproducts')
        return data
    
class VendorPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPrices
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='vendorprices')
        if record_id:
            data['id']=get_rid_pkey('vendorprices')
        return data