from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.sales_credit import SalesCredits
from sales.serializers.credit_serializers import SalesCreditsSerializer


class SalesCreditsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows credits to be modified.
    """
    queryset = SalesCredits.objects.all()
    serializer_class = SalesCreditsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")