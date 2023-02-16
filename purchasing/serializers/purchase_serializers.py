from rest_framework import serializers
from purchasing.models.purchase import *
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='PurchaseOrder')
        if record_id:
            data['id']=get_primary_key('PurchaseOrder')
        return data

class PurchaseOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='PurchaseOrderLines')
        if record_id:
            data['id']=get_primary_key('PurchaseOrderLines')
        return data

class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursment
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}