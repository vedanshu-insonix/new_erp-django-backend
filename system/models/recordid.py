from django.db import models
from .common import BaseContent

class RecordIdentifiers(BaseContent):
    record = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    starting = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    next = models.IntegerField(null=True, blank=True)