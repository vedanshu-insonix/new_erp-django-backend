from rest_framework import viewsets
from warehouse.models.general import *
from warehouse.serializers.general_serializer import *

class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

class JournalTemplateViewSet(viewsets.ModelViewSet):
    queryset = JournalTemplate.objects.all()
    serializer_class = JournalTemplateSerializer

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = Values.objects.all()
    serializer_class = ValueSerializer