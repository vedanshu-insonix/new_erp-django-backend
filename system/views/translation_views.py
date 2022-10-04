from rest_framework import viewsets
from ..models.translations import *
from ..serializers.translation_serializers import *
from django_filters.rest_framework import DjangoFilterBackend

class TranslationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Translations to be modified.
    """
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    