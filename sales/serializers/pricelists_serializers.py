from rest_framework import serializers
from sales.models.pricelist import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

class SalesPriceListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPriceLists
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salespricelists')
        if record_id:
            data['id']=get_rid_pkey('salespricelists')
        return data