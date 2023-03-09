from rest_framework import viewsets
from warehouse.models.routes import *
from warehouse.serializers.route_serializer import *
from rest_framework.response import Response
from system import utils
from warehouse.services.route_services import route_services

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Routes.objects.all()
    serializer_class = RouteSerializer

<<<<<<< HEAD
class RouteTypeViewSet(viewsets.ModelViewSet):
=======
class Route_Type_ViewSet(viewsets.ModelViewSet):
>>>>>>> e770fcc3c25b467b62f54c42a4eda9dad20cc3e3
    queryset = RouteTypes.objects.all()
    serializer_class = RouteTypeSerializer

    def create(self,request):
        route_create = route_services.create_route(self,request)
        if 'success' in route_create:
            ret = route_create['success']
            return Response(utils.success_msg(self,ret))
        else:
            ret = route_create['error']
            return Response(utils.error(self,ret))

<<<<<<< HEAD
class RouteTypeRulesViewSet(viewsets.ModelViewSet):
=======
class Route_Type_Rules_ViewSet(viewsets.ModelViewSet):
>>>>>>> e770fcc3c25b467b62f54c42a4eda9dad20cc3e3
    queryset = RouteTypeRules.objects.all()
    serializer_class = RouteTypeRulesSerializer