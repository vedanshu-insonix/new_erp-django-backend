from rest_framework import serializers
from ..models.customers import Customer
from ..models.address import Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("__all__")
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("__all__")