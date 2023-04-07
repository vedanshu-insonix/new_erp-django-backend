from rest_framework import viewsets
from warehouse.models.operation import *
from warehouse.serializers.operation_serializer import OperationSerializer

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operations.objects.all()
    serializer_class = OperationSerializer