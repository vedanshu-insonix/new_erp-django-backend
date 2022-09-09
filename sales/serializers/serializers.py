from rest_framework import serializers
from ..models.customers import Customer
from ..models.address import Address
from ..models.vendors import Vendor
from system.serializers.common_serializer import CurrencySerializer, StageSerializer, StateSerializer, CountrySerializer, LanguageSerializer


class CustomerSerializer(serializers.ModelSerializer):
    sales_currency = CurrencySerializer(read_only=True, many=False)
    stage = StageSerializer(read_only=True, many=False)
    class Meta:
        model = Customer
        fields = ('__all__')
      

class AddressSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True, many=False)
    country = CountrySerializer(read_only=True, many=False)
    language = LanguageSerializer(read_only=True, many=False)
    stage = StageSerializer(read_only=True, many=False)
    class Meta:
        model = Address
        fields = ("__all__")
            
class VendorSerializer(serializers.ModelSerializer):
    purchasing_currency = CurrencySerializer(read_only=True, many=False)
    stage = StageSerializer(read_only=True, many=False)
    class Meta:
        model = Vendor
        fields = ('__all__')
        

