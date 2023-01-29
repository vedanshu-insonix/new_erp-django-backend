from warehouse.models.products import Locations, Product
from warehouse.serializers.products_serializer import LocationsSerializer, ProductLocationsSerializer

def create_location(self, req):
    ret = {}
    try:
        data=req.data
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
        serializer=LocationsSerializer(data=data, context={'request':req})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        location_id=Locations.objects.get(id=serializer.data.get('id'))
        if have_product == True:
            product_id = product_details.get('product')
            check = Product.objects.filter(id = product_id)
            if check:
                product_details['locations'] = location_id.id
                create_product_location = ProductLocationsSerializer(data=product_details, context={'request':req})
                if create_product_location.is_valid(raise_exception=True):
                    create_product_location.save()
        ret['success'] = serializer.data
        return ret
    except Exception as e:
        ret['error'] = str(e)
        return ret


def update_location(self, req, id):
    ret = {}
    try:
        data=req.data
        location_rec = Locations.objects.get(id=id)
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
        serializer=LocationsSerializer(location_rec, data=data, partial=True, context={'request':req})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        ret['success'] = serializer.data
        return ret
    except Exception as e:
        ret['error'] = str(e)
        return ret