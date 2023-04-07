from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.receipts import Receipts
from sales.serializers.receipts_serializers import ReceiptsSerializer

class ReceiptsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows receipts to be modified.
    """
    queryset = Receipts.objects.all()
    serializer_class = ReceiptsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")