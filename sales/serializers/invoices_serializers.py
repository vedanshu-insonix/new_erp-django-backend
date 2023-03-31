from rest_framework import serializers
from sales.models.invoices import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Sales Invoices Model**************************#
class SalesInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoices
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time", "created_by")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='salesinvoices')
        if record_id:
            data['id']=get_rid_pkey('salesinvoices')
        return super().create(data)