from rest_framework import viewsets
from ..models.manufacturing import *
from ..serializers.manufacturing_serializer import *


class ManufacturingOrderViewSet(viewsets.ModelViewSet):
    queryset = Manufacturing_orders.objects.all()
    serializer_class = ManufacturingOrderSerializer

class ManufacturingOrderLinesViewSet(viewsets.ModelViewSet):
    queryset = Manufacturing_order_lines.objects.all()
    serializer_class = ManufacturingOrderLinesSerializer