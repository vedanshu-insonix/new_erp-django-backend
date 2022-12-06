from rest_framework import viewsets
from warehouse.models.products import *
from warehouse.serializers.products_serializer import *
from warehouse.serializers.general_serializer import AttributesSerializer
from warehouse.models.general import Attributes, Product_Attribute, Journal_Template
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            data = request.data
            have_attr = False
            have_images = False
            if 'attribute' in data:
                attribute_data = data.pop('attribute')
                have_attr=True
            if 'images' in data:
                image_data = data.pop('images')
                have_images = True
            template_name = data.get('template_name')
            if template_name:
                template_rec = Journal_Template.objects.create(journal_template_name=template_name)
                if template_rec:
                    data['template'] = template_rec.id
                    serializer = ProductSerializer(data=data, context={'request':request})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        product_id = Product.objects.get(id = serializer.data.get("id"))
                        if have_images == True:
                            for image in image_data:
                                image_rec = Images.objects.create(image=image, title=template_name, file=image)
                                Product_Images.objects.create(product= product_id, image=image_rec)
                        if have_attr==True:
                            for attributes in attribute_data:
                                attr_id = Attributes.objects.filter(attribute=attributes)
                                if attr_id:
                                    attr_id = Attributes.objects.get(attribute=attributes)
                                    pass
                                else:
                                    attr_id = Attributes.objects.create(attribute=attributes)
                                createproductattribute = Product_Attribute.objects.create(product=product_id, attribute=attr_id)
                                check = Value.objects.filter(value=attribute_data[attributes], attribute=attr_id)
                                if check:
                                    value_id = Value.objects.get(value=attribute_data[attributes], attribute=attr_id)
                                    pass
                                else:
                                    value_id = Value.objects.create(value=attribute_data[attributes], attribute=attr_id)
                                createproductValue = Product_Values.objects.create(product=product_id, value=value_id)
                        product_rec = Product.objects.get(id = product_id.id)
                        return_data = ProductSerializer(product_rec, context={'request': request})
                        return Response(return_data.data)
            else:
                msg = 'please enter a valid template name'
                response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': msg}
                return Response(response)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)

    def update(self,request,pk=None):
        try:
            data = request.data
            product_rec = Product.objects.get(id=pk)
            updateproduct = ProductSerializer(product_rec, data=data, context={'request': request})
            if updateproduct.is_valid():
                updateproduct.save()
                if 'template_name' in data:
                    template_rec = Journal_Template.objects.filter(id = product_rec.template.id)
                    template_rec = template_rec.update(journal_template_name=data.get('template_name'))

            product_rec = Product.objects.get(id = pk)
            return_data = ProductSerializer(product_rec, context={'request': request})
            return Response(return_data.data)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)

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

class UOMViewSet(viewsets.ModelViewSet):
    queryset = UOM.objects.all()
    serializer_class = UOMSerializer