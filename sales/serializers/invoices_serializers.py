from rest_framework import serializers
from sales.models.invoices import *

class SalesInvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoices
        fields = ('__all__')