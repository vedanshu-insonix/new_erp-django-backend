from rest_framework import serializers
from purchasing.models.manufacturing import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

class ManufacturingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorders
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='manufacturingorders')
        if record_id:
            data['id']=get_rid_pkey('manufacturingorders')
        return data

class ManufacturingOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorderlines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='manufacturingorderlines')
        if record_id:
            data['id']=get_rid_pkey('manufacturingorderlines')
        return data