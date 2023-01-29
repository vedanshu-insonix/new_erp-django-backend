from warehouse.models.products import Product, Value, Product_Values
from warehouse.models.general import Attributes, Product_Attribute


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
            Product_Attribute.objects.create(product=product_id, attribute=attr_id)
        check = Value.objects.filter(value=variant_values[attr], attribute=attr_id)
        if check:
            value_id = Value.objects.get(value=variant_values[attr], attribute=attr_id)
        else:
            value_id = Value.objects.create(value=variant_values[attr], attribute=attr_id)
        check = Product_Values.objects.filter(product=product_id, value=value_id)
        if check:
            continue
        else:
            Product_Values.objects.create(product=product_id, value=value_id)
    return True