from rest_framework import serializers
from sales.models.carts import *

class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('__all__')

class CartlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartlines
        fields = ('__all__')