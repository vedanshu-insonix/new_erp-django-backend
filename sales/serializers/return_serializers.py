from rest_framework import serializers
from sales.models.returns import *
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers

class SalesReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturns
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='SalesReturns')
        if record_id:
            data['id']=get_primary_key('SalesReturns')
        return data

class SalesReturnLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturnLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='SalesReturnLines')
        if record_id:
            data['id']=get_primary_key('SalesReturnLines')
        return data