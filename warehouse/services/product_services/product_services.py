from warehouse.models.products import Product
from warehouse.serializers.products_serializer import ProductSerializer
from warehouse.models.general import Images, ProductImages
from .product_common_services import create_attribute
from system.views.common_views import extracting_data


def create_product(self, req):
    res = {}
    try:
        data = req.data
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
                    serializer = ProductSerializer(data=data, context={'request':req})
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    product_id = Product.objects.get(id = serializer.data.get("id"))
                    if have_images == True:
                        for image in image_data:
                            image_rec = Images.objects.create(image=image, title=template_name, file=image)
                            ProductImages.objects.create(product= product_id, image=image_rec)
                    create_attribute(variant_values,product_id.id)
                    template = Product.objects.get(id=product_id.id)
                    response=ProductSerializer(template, context={'request': req})
                    result.append(response.data)
            else:
                data['variant_name']=f'[{stock_num}] {temp_variant_name}'
                if template_name:
                    template_exists=Product.objects.filter(template_name=template_name)
                    if template_exists:
                        data['template'] = template_exists.values()[0]['id']
                serializer = ProductSerializer(data=data, context={'request':req})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    result.append(serializer.data)   
            res["success"] = result
            return res
        else:
            msg = 'please enter a valid record detail.'
            res["error"] = msg
            return res
    except Exception as e:
        res["error"] = str(e)
        return res


def bulk_upload(self, req):
    ret = {}
    try:
        template_file = req.FILES.get('template_file')
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
                        serializer=ProductSerializer(data=data_dict[i], context={'request':req})
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
                ret["success_def"] = template_count
                ret["defect"] = defective_data
                return ret
            else:
                ret["success"] = template_count
                return ret
        else:
            msg="Please Upload A Suitable Excel File."
            ret["error"] = msg
            return ret
    except Exception as e:
        ret["error"] = str(e)
        return ret