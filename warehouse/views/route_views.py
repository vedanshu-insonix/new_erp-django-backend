from rest_framework import viewsets
from warehouse.models.routes import *
from warehouse.serializers.route_serializer import *
from rest_framework.response import Response
from system import utils
from warehouse.serializers.operation_serializer import Operation_Serializer

class Route_ViewSet(viewsets.ModelViewSet):
    queryset = Routes.objects.all()
    serializer_class = Route_Serializer

    def create(self,request):
        try:
            data=request.data
            have_steps = False
            if 'steps' in data:
                steps = data.pop('steps')
                have_steps = True
            route_name=data.get('route_type')
            if route_name:
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
                serializer = Route_Serializer(data=data, context={'request':request})
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                route_id = serializer.data.get('id')
                if have_steps == True:
                    for step in steps:
                        step['route'] = route_id
                        step_serializer = Operation_Serializer(data=step, context={'request':request})
                        if step_serializer.is_valid(raise_exception=True):
                            step_serializer.save()
            new_route_rec = Routes.objects.get(id=route_id)
            result = Route_Serializer(new_route_rec)
            return Response(utils.success_msg(self,result.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

class Route_Type_ViewSet(viewsets.ModelViewSet):
    queryset = Route_Types.objects.all()
    serializer_class = Route_Type_Serializer

    def create(self,request):
        try:
            data=request.data
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
            serializer = Route_Type_Serializer(data=data,context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(utils.success_msg(self,serializer.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

class Route_Type_Rules_ViewSet(viewsets.ModelViewSet):
    queryset = Route_Type_Rules.objects.all()
    serializer_class = Route_Type_Rules_Serializer