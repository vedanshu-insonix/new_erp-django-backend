from rest_framework import serializers
from warehouse.models.shipping_models import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

class DeliveriesSerializer(serializers.ModelSerializer):
    class meta:
        model = Deliveries
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='deliveries')
        if record_id:
            data['id']=get_rid_pkey('deliveries')
        return data

class DeliveryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='deliverylines')
        if record_id:
            data['id']=get_rid_pkey('deliverylines')
        return data

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='shipments')
        if record_id:
            data['id']=get_rid_pkey('shipments')
        return data

class ContainerTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerTypes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='containertypes')
        if record_id:
            data['id']=get_rid_pkey('containertypes')
        return data

class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='containers')
        if record_id:
            data['id']=get_rid_pkey('containers')
        return data

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='contents')
        if record_id:
            data['id']=get_rid_pkey('contents')
        return data