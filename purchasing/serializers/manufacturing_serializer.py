from rest_framework import serializers
from purchasing.models.manufacturing import *
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers

class ManufacturingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorders
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Manufacturingorders')
        if record_id:
            data['id']=get_primary_key('Manufacturingorders')
        return data

class ManufacturingOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorderlines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Manufacturingorderlines')
        if record_id:
            data['id']=get_primary_key('Manufacturingorderlines')
        return data