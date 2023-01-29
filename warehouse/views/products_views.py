from rest_framework import viewsets
from warehouse.models.products import *
from warehouse.serializers.products_serializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from system import utils
from warehouse.services.product_services import product_services, attribute_services
from warehouse.services.location_services import location_services

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    @action(detail=False, methods=['GET'], name='template')
    def get_template(self):
        try:
            template_rec = Product.objects.filter(id = 1)
            serializer = RelatedProductSerializer(template_rec, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(utils.error(self,str(e)))

    def create(self, request):
        prod_create = product_services.create_product(self,request)
        if 'success' in prod_create:
            ret = prod_create['success']
            return Response(utils.success_msg(self,ret))
        else:
            ret = prod_create['error']
            return Response(utils.error(self,ret))

    @action(detail=True, methods=['post'],url_path = "add_attributes")
    def add_attributes(self,request,pk=None):
        create_attribute = attribute_services.add_attributes(self, request, pk)
        if 'success' in create_attribute:
            ret = create_attribute['success']
            return Response(ret)
        else:
            ret = create_attribute['error']
            return Response(utils.error(self,ret))

    @action(detail=True, methods=['post'], url_path='remove_attributes')
    def remove_attributes(self,request,pk=None):
        del_attr = attribute_services.delete_attribute(self, request, pk)
        if 'success' in del_attr:
            ret = del_attr['success']
            return Response(ret)
        else:
            ret = del_attr['error']
            return Response(utils.error(self,ret))

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        bulk_upload = product_services.bulk_upload(self, request)
        if 'success' in bulk_upload:
            ret = bulk_upload['success']
            return Response(utils.success(self,ret))
        else:
            if 'success' in bulk_upload:
                success_def = bulk_upload['success_def']
                defect = bulk_upload['defect']
                return Response(utils.success_def(self,success_def,defect))
            else:
                ret = bulk_upload['error']
                return Response(utils.error(self,ret))

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

    def create(self,request):
        loc_create = location_services.create_location(self, request)
        if 'success' in loc_create:
            ret = loc_create['success']
            return Response(utils.success_msg(self,ret))
        else:
            ret = loc_create['error']
            return Response(utils.error(self,ret))

    def update(self,request,pk):
        loc_update = location_services.update_location(self, request, pk)
        if 'success' in loc_update:
            ret = loc_update['success']
            return Response(utils.success_msg(self,ret))
        else:
            ret = loc_update['error']
            return Response(utils.error(self,ret))

class ProductCountsViewSet(viewsets.ModelViewSet):
    queryset = ProductCounts.objects.all()
    serializer_class = ProductCountsSerializer

class ProductLocationsViewSet(viewsets.ModelViewSet):
    queryset = ProductLocations.objects.all()
    serializer_class = ProductLocationsSerializer

class UOMViewSet(viewsets.ModelViewSet):
    queryset = UOM.objects.all()
    serializer_class = UOMSerializer