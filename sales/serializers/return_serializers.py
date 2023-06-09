from rest_framework import serializers
from sales.models.returns import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Sales Returns Model**************************#
class SalesReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturns
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salesreturns')
        if record_id:
            data['id']=get_rid_pkey('salesreturns')
        return super().create(data)

#**************************Serializer For Sales Return Lines Model**************************#
class SalesReturnLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturnLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salesreturnlines')
        if record_id:
            data['id']=get_rid_pkey('salesreturnlines')
        return super().create(data)