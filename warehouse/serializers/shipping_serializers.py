from rest_framework import serializers
from warehouse.models.shipping_models import *

class DeliveriesSerializer(serializers.ModelSerializer):
    class meta:
        model = Deliveries
        fields = ('__all__')

class DeliveryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLines
        fields = ('__all__')

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ('__all__')

class ContainerTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerTypes
        fields = ('__all__')

class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        fields = ('__all__')

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ('__all__')