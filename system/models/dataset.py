from django.db import models
from .common import BaseContent

class DataTable(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    system_name=models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)

class Data(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    data_source=models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True, blank=True)
    name= models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)