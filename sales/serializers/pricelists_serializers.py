from rest_framework import serializers
from sales.models.pricelist import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Sales Price Lists Model**************************#
class SalesPriceListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPriceLists
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salespricelists')
        if record_id:
            data['id']=get_rid_pkey('salespricelists')
        return super().create(data)