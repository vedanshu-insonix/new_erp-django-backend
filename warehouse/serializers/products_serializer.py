from attr import field
from rest_framework import serializers
from erp_system.warehouse.models.products import *

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        field = ('__all__')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = ('__all__')

class BomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bom
        field = ('__all__')

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        field = ('__all__')

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        field = ('__all__')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        field = ('__all__')

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        field = ('__all__')

class EquivalentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equivalents
        field = ('__all__')

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        field = ('__all__')

class ProductCountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCounts
        field = ('__all__')

class ProductLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLocations
        field = ('__all__')