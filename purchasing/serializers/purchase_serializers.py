from rest_framework import serializers
from purchasing.models.purchase import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Purchase Order Model**************************#
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='purchaseorder')
        if record_id:
            data['id']=get_rid_pkey('purchaseorder')
        return super().create(data)

#**************************Serializer For Purchase Order Lines Model**************************#
class PurchaseOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='purchaseorderlines')
        if record_id:
            data['id']=get_rid_pkey('purchaseorderlines')
        return super().create(data)

#**************************Serializer For Disbursement Model**************************#
class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursment
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='disbursment')
        if record_id:
            data['id']=get_rid_pkey('disbursment')
        return super().create(data)