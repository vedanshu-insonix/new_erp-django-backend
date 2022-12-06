from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.returns import SalesReturns, SalesReturnLines
from sales.serializers.return_serializers import SalesReturnsSerializer, SalesReturnLinesSerializer


class SalesReturnsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows returns to be modified.
    """
    queryset = SalesReturns.objects.all()
    serializer_class = SalesReturnsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class SalesReturnLinesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows return lines to be modified.
    """
    queryset = SalesReturnLines.objects.all()
    serializer_class = SalesReturnLinesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")