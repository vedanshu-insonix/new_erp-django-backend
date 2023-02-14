from django.db import models
from .common import BaseContent

class Table(BaseContent):
    table=models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)

class Data(BaseContent):
    dataset=models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    name= models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)
    data_type = models.CharField(max_length = 255, null=True, blank=True)
    field= models.CharField(max_length = 255, null=True, blank=True)
    field_type= models.CharField(max_length = 255, null=True, blank=True)
    comment=models.TextField(null=True, blank=True)
    
    
# class Dataset(BaseContent):
#     name = models.CharField(max_length=255, null=True, blank= True)
#     description=models.TextField(null=True, blank=True)
#     #entity = models.ForeignKey('system.Entity', on_delete=models.SET_NULL, null=True, blank=True)