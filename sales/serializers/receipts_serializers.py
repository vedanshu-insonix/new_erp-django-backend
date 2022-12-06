from rest_framework import serializers
from sales.models.receipts import *

class ReceiptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipts
        fields = ('__all__')