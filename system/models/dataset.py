from django.db import models
from .common import BaseContent

class Table(BaseContent):
    table=models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)

class Data(BaseContent):
    table=models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    name= models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)