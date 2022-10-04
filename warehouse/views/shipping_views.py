from rest_framework import viewsets
from warehouse.models.shipping_models import *
from warehouse.serializers.shipping_serializers import *
# Create your views here.

class DeliveriesViewSet(viewsets.ModelViewSet):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveriesSerializer

class DeliveryLinesViewSet(viewsets.ModelViewSet):
    queryset = DeliveryLines.objects.all()
    serializer_class = DeliveryLinesSerializer

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipments.objects.all()
    serializer_class = ShipmentSerializer

class ContainerTypesViewSet(viewsets.ModelViewSet):
    queryset = ContainerTypes.objects.all()
    serializer_class = ContainerTypesSerializer

class ContainersViewSet(viewsets.ModelViewSet):
    queryset = Containers.objects.all()
    serializer_class = ContainersSerializer

class ContentsViewSet(viewsets.ModelViewSet):
    queryset = Contents.objects.all()
    serializer_class = ContentsSerializer