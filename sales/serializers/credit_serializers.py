from rest_framework import serializers
from sales.models.sales_credit import *

class SalesCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCredits
        fields = ('__all__')