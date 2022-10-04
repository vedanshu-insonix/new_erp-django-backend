from rest_framework import serializers
from warehouse.models.shipping_models import *

class DeliveriesSerializer(serializers.ModelSerializer):
    class meta:
        model = Deliveries
        field = ('__all__')

class DeliveryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLines
        field = ('__all__')

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        field = ('__all__')

class ContainerTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerTypes
        field = ('__all__')

class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        field = ('__all__')

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        field = ('__all__')