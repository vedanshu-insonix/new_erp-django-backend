from rest_framework import viewsets, filters
from ..serializers.recordid_serializers import *
from ..models.recordid import *
from django_filters.rest_framework import DjangoFilterBackend

class RecordIdentifierViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Record ID to be modified.
    """
    queryset = RecordIdentifiers.objects.all()
    serializer_class = RecordIdentifierSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")