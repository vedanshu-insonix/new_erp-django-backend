from rest_framework import serializers
from sales.models.sales_credit import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Sales Credits Model**************************#
class SalesCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCredits
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salescredits')
        if record_id:
            data['id']=get_rid_pkey('salescredits')
        return super().create(data)