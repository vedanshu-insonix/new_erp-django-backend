from warehouse.models.products import Product, Value, Product_Values
from warehouse.serializers.products_serializer import ProductSerializer
from .product_common_services import create_attribute
from warehouse.models.general import Attributes, Product_Attribute

def add_attributes(self,req,id):
    ret = {}
    try:
        data=req.data
        product_rec = Product.objects.get(id=id)
        create_attribute(data,id)
        editted_rec = Product.objects.get(id=id)
        serializer=ProductSerializer(editted_rec, context={'request': req})
        ret['success'] = serializer.data
        return ret
    except Exception as e:
        ret['error'] = str(e)
        return ret

def delete_attribute(self, req, id):
    ret = {}
    try:
        data=req.data
        product_rec = Product.objects.get(id=id)
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
        editted_rec = Product.objects.get(id=id)
        serializer=ProductSerializer(editted_rec, context={'request': req})
        ret['success'] = serializer.data
        return ret
    except Exception as e:
        ret['error'] = str(e)
        return ret