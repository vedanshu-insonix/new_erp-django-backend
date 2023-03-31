from rest_framework import serializers
from warehouse.models.operation import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Operations Model**************************#
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='operations')
        if record_id:
            data['id']=get_rid_pkey('operations')
        return super().create(data)
    