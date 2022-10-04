from rest_framework import viewsets
from ..serializers.company_serializers import *
from ..models.company import *
from django_filters.rest_framework import DjangoFilterBackend


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")