from rest_framework import viewsets
from warehouse.models.products import *
from warehouse.serializers.products_serializer import *
from warehouse.serializers.general_serializer import AttributesSerializer
from warehouse.models.general import Attributes, Product_Attribute, Journal_Template
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from system import utils
from system.views.common_views import extracting_data

def create_attribute(variant_values,temp_id):
    product_id=Product.objects.get(id=temp_id)
    for attr in variant_values:
        attr_id = Attributes.objects.filter(attribute=attr)
        if attr_id:
            attr_id = Attributes.objects.get(attribute=attr)
        else:
            attr_id = Attributes.objects.create(attribute=attr)
        check = Product_Attribute.objects.filter(product=product_id, attribute=attr_id)
        if check:
            continue
        else:
            createproductattribute = Product_Attribute.objects.create(product=product_id, attribute=attr_id)
        check = Value.objects.filter(value=variant_values[attr], attribute=attr_id)
        if check:
            value_id = Value.objects.get(value=variant_values[attr], attribute=attr_id)
        else:
            value_id = Value.objects.create(value=variant_values[attr], attribute=attr_id)
        check = Product_Values.objects.filter(product=product_id, value=value_id)
        if check:
            continue
        else:
            createproductValue = Product_Values.objects.create(product=product_id, value=value_id)
    return True

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    @action(detail=False, methods=['GET'], name='template')
    def get_template(self,request):
        try:
            template_rec = Product.objects.filter(id = 1)
            serializer = RelatedProductSerializer(template_rec, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(utils.error(self,str(e)))

    def create(self, request):
        try:
            data = request.data
            have_attr = False
            have_images = False
            string = ""
            if 'attribute' in data:
                attribute_data = data.pop('attribute')
                have_attr=True    
            if 'images' in data:
                image_data = data.pop('images')
                have_images = True
            template_name = data.get('template_name')
            stock_num = data.get('stock_number')
            temp_variant_name = data.get('template_variant_name')
            result = []
            if (template_name or data.get('template')):
                if have_attr == True:
                    for variant_values in attribute_data:
                        values = []
                        for attributes in variant_values:
                            values.append(variant_values[attributes])
                        string = ", ".join (map (str, values))
                        if string == "":
                            data['variant_name']=f'[{stock_num}] {temp_variant_name}'
                        else:
                            data['variant_name']=f'[{stock_num}] {temp_variant_name}, {string}'
                        if template_name:
                            template_exists=Product.objects.filter(template_name=template_name)
                            if template_exists:
                                data['template'] = template_exists.values()[0]['id']
                        serializer = ProductSerializer(data=data, context={'request':request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                        product_id = Product.objects.get(id = serializer.data.get("id"))
                        if have_images == True:
                            for image in image_data:
                                image_rec = Images.objects.create(image=image, title=template_name, file=image)
                                Product_Images.objects.create(product= product_id, image=image_rec)
                        create_attribute(variant_values,product_id.id)
                        template = Product.objects.get(id=product_id.id)
                        response=ProductSerializer(template, context={'request': request})
                        result.append(response.data)
                else:
                    data['variant_name']=f'[{stock_num}] {temp_variant_name}'
                    if template_name:
                        template_exists=Product.objects.filter(template_name=template_name)
                        if template_exists:
                            data['template'] = template_exists.values()[0]['id']
                    serializer = ProductSerializer(data=data, context={'request':request})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        result.append(serializer.data)   
                return Response(utils.success_msg(self,result))   
            else:
                msg = 'please enter a valid record detail.'
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

    @action(detail=True, methods=['post'],url_path = "add_attributes")
    def add_attributes(self,request,pk=None):
        try:
            data=request.data
            product_rec = Product.objects.get(id=pk)
            create_attribute(data,pk)
            editted_rec = Product.objects.get(id=pk)
            serializer=ProductSerializer(editted_rec, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response(utils.error(self,str(e)))

    @action(detail=True, methods=['post'], url_path='remove_attributes')
    def remove_attributes(self,request,pk=None):
        try:
            data=request.data
            product_rec = Product.objects.get(id=pk)
            for attributes in data:
                attr_rec = Attributes.objects.get(attribute = attributes)
                if attr_rec:
                    attr = Product_Attribute.objects.get(product=product_rec, attribute=attr_rec)
                    if attr:
                        attr.delete()
                    value_rec = Value.objects.get(value=data[attributes], attribute=attr_rec)
                    if value_rec:
                        check = Product_Values.objects.get(product=product_rec, value=value_rec)
                        if check:
                            check.delete()
            editted_rec = Product.objects.get(id=pk)
            serializer=ProductSerializer(editted_rec, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response(utils.error(self,str(e)))

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            template_file = request.FILES.get('template_file')
            if template_file:
                data_dict = extracting_data(template_file)
                template_count = 0
                defective_data=[]
                attr_dict={}
                for i in range(len(data_dict)):
                    if data_dict[i] != None:

                        values=(data_dict[i].pop('values')).split(',')
                        attributes=(data_dict[i].pop('attributes')).split(',')
                        stock_num=data_dict[i]['stock_number']
                        template_variant_name=data_dict[i]['template_variant_name']
                        data_dict[i]['variant_name']=f'[{stock_num}]{template_variant_name},{values}'
                        template_name=data_dict[i]['template_name']
                        
                        template_id=Product.objects.filter(template_name__icontains=template_name)
                        if template_id:
                            template_id=template_id.values()[0]['id']
                            data_dict[i]['template']=template_id
                        temp_rec=Product.objects.filter(template_name__icontains=template_name, variant_name=data_dict[i]['variant_name'])
                        if temp_rec:
                            product_id=temp_rec.values()[0]['id']
                            defective_data.append(template_name)
                        else:
                            serializer=ProductSerializer(data=data_dict[i], context={'request':request})
                            if serializer.is_valid(raise_exception=True):
                                serializer.save()
                                template_count+=1
                            product_id=serializer.data.get('id')            
                        for i in range(len(attributes)):
                            attr_dict[attributes[i]]=values[i]
                        if attr_dict:
                            create_attribute(attr_dict,product_id)
                if defective_data:
                    defective_data = {
                        "duplicate_templates" : f"These {set(defective_data)} templates are already exists."
                    } 
                    return Response(utils.success_def(self,template_count,defective_data))
                else:
                    return Response(utils.success(self,template_count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

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
        try:
            data=request.data
            have_product = False
            location_name=data.get('locations_name')
            tokens=location_name.split("/")
            string=""
            for word in tokens:
                new_text = word.split()
                for text in new_text:
                    if (text.isnumeric())|(len(text) == 2):
                        string += str(text)
                    else:
                        string += str(text[0])
                if (len(tokens) == 1)|(word == tokens[-1]):
                    pass
                else:
                    string+='/'
            data['code']=string.upper()
            parent_id = data.get('parent')
            if parent_id:
                parent_data = Locations.objects.get(id=parent_id)
                address_id = parent_data.loc_address
                data['loc_address'] = address_id
            if 'product' in data:
                product_details = data.pop('product')
                have_product = True
            serializer=LocationsSerializer(data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            location_id=Locations.objects.get(id=serializer.data.get('id'))
            if have_product == True:
                product_id = product_details.get('product')
                check = Product.objects.filter(id = product_id)
                if check:
                    product_details['locations'] = location_id.id
                    create_product_location = ProductLocationsSerializer(data=product_details, context={'request':request})
                    if create_product_location.is_valid(raise_exception=True):
                        create_product_location.save()
            return Response(utils.success_msg(self,serializer.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

    def update(self,request,pk):
        try:
            data=request.data
            location_rec = Locations.objects.get(id=pk)
            if 'location_name' in data:
                location_name=data.get('locations_name')
                tokens=location_name.split("/")
                string=""
                for word in tokens:
                    new_text = word.split()
                    for text in new_text:
                        if (text.isnumeric())|(len(text) == 2):
                            string += str(text)
                        else:
                            string += str(text[0])
                    if (len(tokens) == 1)|(word == tokens[-1]):
                        pass
                    else:
                        string+='/'
                data['code']=string.upper()
            serializer=LocationsSerializer(location_rec, data=data, partial=True, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(utils.success_msg(self,serializer.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

class ProductCountsViewSet(viewsets.ModelViewSet):
    queryset = ProductCounts.objects.all()
    serializer_class = ProductCountsSerializer

class ProductLocationsViewSet(viewsets.ModelViewSet):
    queryset = ProductLocations.objects.all()
    serializer_class = ProductLocationsSerializer

class UOMViewSet(viewsets.ModelViewSet):
    queryset = UOM.objects.all()
    serializer_class = UOMSerializer