from rest_framework import serializers
from sales.models.pricelist import *

class SalesPriceListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPriceLists
        fields = ('__all__')