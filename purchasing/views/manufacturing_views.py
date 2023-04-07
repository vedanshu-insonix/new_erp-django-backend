from rest_framework import viewsets
from ..models.manufacturing import *
from ..serializers.manufacturing_serializer import *


class ManufacturingOrderViewSet(viewsets.ModelViewSet):
    queryset = Manufacturingorders.objects.all()
    serializer_class = ManufacturingOrderSerializer

class ManufacturingOrderLinesViewSet(viewsets.ModelViewSet):
    queryset = Manufacturingorderlines.objects.all()
    serializer_class = ManufacturingOrderLinesSerializer