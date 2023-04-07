from warehouse.serializers.route_serializer import RouteTypeSerializer

def create_route(self, req):
    ret = {}
    try:
        data=req.data
        route_name=data.get('name')
        tokens=route_name.split(",")
        string=""
        for word in tokens:
            new_text = word.split()
            for text in new_text:
                if (text.isnumeric()):
                    string += str(text)
                else:
                    if text == 'to':
                        pass
                    else:
                        string += str(text[0])
        data['code']=string.upper()
        serializer = RouteTypeSerializer(data=data,context={'request':req})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        ret['success'] = serializer.data
        return ret
    except Exception as e:
        ret['error'] = str(e)
        return ret