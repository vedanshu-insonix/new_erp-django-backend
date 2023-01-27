from rest_framework import serializers
from purchasing.models.manufacturing import *

class ManufacturingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturing_orders
        fields = ('__all__')

class ManufacturingOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturing_order_lines
        fields = ('__all__')