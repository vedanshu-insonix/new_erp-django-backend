from rest_framework import serializers
from warehouse.models.products import *
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.common_serializers import RelatedStageSerializer, RelatedConfigurationSerializer, RelatedChoiceSerializer
from warehouse.models.general import *
from warehouse.serializers.general_serializer import *
from sales.serializers.addresses_serializers import AddressSerializer
from warehouse.serializers.route_serializer import Route_Serializer

#******************************* Product Serializer *******************************
class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("created_time","modified_time","created_by")

class ProductSerializer(serializers.ModelSerializer):
    attribute = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_attribute(self, obj):
        queryset = Product_Attribute.objects.filter(product=obj.id)
        serializer = ProductAttributeSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['attribute']) if serializer.data else None
        return result

    def get_value(self, obj):
        queryset = Product_Values.objects.filter(product = obj.id)
        serializer = ProductValueSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['value']) if serializer.data else None
        return result

    def get_image(self, obj):
        queryset = Product_Images.objects.filter(product = obj.id)
        serializer = ProductImagesSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['image']) if serializer.data else None
        return result

    class Meta:
        model = Product
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        
        stocking_unit = UOMSerializer(instance.stocking_unit, context={'request': request}).data
        if 'id' in stocking_unit:
            response['stocking_unit'] = UOMSerializer(instance.stocking_unit, context={'request': request}).data
        product_type = RelatedConfigurationSerializer(instance.product_type, context={'request': request}).data
        if 'id' in product_type:
            response['product_type'] = RelatedConfigurationSerializer(instance.product_type, context={'request': request}).data
        stage = RelatedStageSerializer(instance.stage, context={'request': request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        status_choices = RelatedChoiceSerializer(instance.status_choices, context={'request': request}).data
        if 'id' in status_choices:
            response['status_choices'] = RelatedChoiceSerializer(instance.status_choices, context={'request': request}).data
        parent_data = RelatedProductSerializer(instance.template).data
        if 'id' in parent_data:
            response['template'] = RelatedProductSerializer(instance.template).data
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

class BomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bom
        fields = ('__all__')

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ('__all__')

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = ('__all__')

class RelatedValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        exclude = ("created_time","modified_time","created_by")

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

class ProductValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Values
        fields = ('value',)
        depth = 1

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('__all__')

class EquivalentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equivalents
        fields = ('__all__')

class RelatedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ("id","locations_name", "code")

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)

        parent_data = RelatedLocationSerializer(instance.parent_location).data
        if 'id' in parent_data:
            response['parent_location'] = RelatedLocationSerializer(instance.parent_location).data
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        loc_address = AddressSerializer(instance.loc_address).data
        if 'id' in loc_address:
            response['loc_address'] = AddressSerializer(instance.loc_address).data
        return response

class ProductCountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCounts
        fields = ('__all__')

class ProductLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLocations
        fields = ('__all__')

class UOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UOM
        fields = ('__all__')