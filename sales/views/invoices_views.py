from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.invoices import SalesInvoices
from sales.serializers.invoices_serializers import SalesInvoicesSerializer


class SalesInvoicesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows invoices to be modified.
    """
    queryset = SalesInvoices.objects.all()
    serializer_class = SalesInvoicesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")