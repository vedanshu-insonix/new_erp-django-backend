from django.db import models
from .common import BaseContent
from system.utils import Column_Visibility_Choice
    
class Column(BaseContent):
    list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True)
    column = models.CharField(max_length=255, null=True, blank=True)
    table = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    #default = models.BooleanField(default=False)
    #required = models.BooleanField(default = False)
    #optional = models.BooleanField(default = False)
    visibility = models.CharField(max_length=255, choices=Column_Visibility_Choice, null=True, blank=True)
    
    
    def __str__(self):
        return self.column
    
