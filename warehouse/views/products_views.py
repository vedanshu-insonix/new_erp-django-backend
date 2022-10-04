from rest_framework import viewsets
from erp_system.warehouse.models.products import *
from warehouse.serializers.products_serializer import *

class TamplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BOMViewSet(viewsets.ModelViewSet):
    queryset = Bom.objects.all()
    serializer_class = BomSerializer

class ComponentsViewSet(viewsets.ModelViewSet):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer

class CharacteristicsViewSet(viewsets.ModelViewSet):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class EquivalentsViewSet(viewsets.ModelViewSet):
    queryset = Equivalents.objects.all()
    serializer_class = EquivalentsSerializer

class LocationsViewSet(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

class ProductCountsViewSet(viewsets.ModelViewSet):
    queryset = ProductCounts.objects.all()
    serializer_class = ProductCountsSerializer

class ProductLocationsViewSet(viewsets.ModelViewSet):
    queryset = ProductLocations.objects.all()
    serializer_class = ProductLocationsSerializer