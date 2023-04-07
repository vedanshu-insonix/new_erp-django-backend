from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.pricelist import SalesPriceLists
from sales.serializers.pricelists_serializers import SalesPriceListsSerializer


class SalesPriceListsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows pricelists to be modified.
    """
    queryset = SalesPriceLists.objects.all()
    serializer_class = SalesPriceListsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")