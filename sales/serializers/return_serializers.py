from rest_framework import serializers
from sales.models.returns import *

class SalesReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturns
        fields = ('__all__')

class SalesReturnLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturnLines
        fields = ('__all__')