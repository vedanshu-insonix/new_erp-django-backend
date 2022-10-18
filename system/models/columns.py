from django.db import models
from .common import BaseContent
from system.utils import ColumnTypeChoice, StatusChoice


class App(BaseContent):
    name = models.CharField(max_length=255, null=True)    
    def __str__(self):
        return str(self.id)
    
    
class Column(BaseContent):
    list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True)
    column = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    default = models.BooleanField(default=False)
    required = models.BooleanField(default = False)
    optional = models.BooleanField(default = False)
    
    
    def __str__(self):
        return self.column
    
