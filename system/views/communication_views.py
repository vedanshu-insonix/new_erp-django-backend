from rest_framework import viewsets
from ..serializers.communication_serializers import *
from ..models.communication import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ChannelViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    

class CommunicationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

