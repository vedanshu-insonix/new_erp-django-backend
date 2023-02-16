from rest_framework import serializers
from sales.models.receipts import *
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers

class ReceiptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipts
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Receipts')
        if record_id:
            data['id']=get_primary_key('Receipts')
        return data