from rest_framework import serializers
from purchasing.models.purchase import *

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('__all__')

class PurchaseOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderLines
        fields = ('__all__')

class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursment
        fields = ('__all__')