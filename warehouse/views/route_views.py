from rest_framework import viewsets
from warehouse.models.routes import *
from warehouse.serializers.route_serializer import *
from rest_framework.response import Response
from system import utils
from warehouse.services.route_services import route_services

class Route_ViewSet(viewsets.ModelViewSet):
    queryset = Routes.objects.all()
    serializer_class = Route_Serializer

class Route_Type_ViewSet(viewsets.ModelViewSet):
    queryset = Route_Types.objects.all()
    serializer_class = Route_Type_Serializer

    def create(self,request):
        route_create = route_services.create_route(self,request)
        if 'success' in route_create:
            ret = route_create['success']
            return Response(utils.success_msg(self,ret))
        else:
            ret = route_create['error']
            return Response(utils.error(self,ret))

class Route_Type_Rules_ViewSet(viewsets.ModelViewSet):
    queryset = Route_Type_Rules.objects.all()
    serializer_class = Route_Type_Rules_Serializer