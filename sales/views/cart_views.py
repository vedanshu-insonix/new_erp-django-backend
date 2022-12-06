from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.carts import Carts, Cartlines
from sales.serializers.cart_serializers import CartsSerializer, CartlinesSerializer


class CartsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Carts to be modified.
    """
    queryset = Carts.objects.all()
    serializer_class = CartsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class CartlinesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Cartlines to be modified.
    """
    queryset = Cartlines.objects.all()
    serializer_class = CartlinesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")