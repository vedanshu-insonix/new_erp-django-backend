from django.db import models
from .common import BaseContent
    
class Column(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True)
    column = models.CharField(max_length=255, null=True, blank=True)
    table = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    visibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return self.column
    
