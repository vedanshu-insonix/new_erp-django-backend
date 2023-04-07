from rest_framework import serializers
from purchasing.models.manufacturing import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Manufacturing Order Model**************************#
class ManufacturingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorders
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='manufacturingorders')
        if record_id:
            data['id']=get_rid_pkey('manufacturingorders')
        return super().create(data)

#**************************Serializer For Manufacturing Order Lines Model**************************#
class ManufacturingOrderLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturingorderlines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='manufacturingorderlines')
        if record_id:
            data['id']=get_rid_pkey('manufacturingorderlines')
        return super().create(data)