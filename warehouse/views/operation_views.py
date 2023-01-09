from rest_framework import viewsets
from warehouse.models.operation import *
from warehouse.serializers.operation_serializer import *

class Operation_ViewSet(viewsets.ModelViewSet):
    queryset = Operations.objects.all()
    serializer_class = Operation_Serializer