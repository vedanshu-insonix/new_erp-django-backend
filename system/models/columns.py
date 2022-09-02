from django.db import models
from .common import BaseContent
from system.utils import ColumnTypeChoice, StatusChoice




class App(BaseContent):
    name = models.CharField(max_length=255, null=True)    
    def __str__(self):
        return self.name
    
class Module(BaseContent):
    app = models.ForeignKey('App', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name

class Columns(BaseContent):
    app = models.ForeignKey('App', on_delete=models.CASCADE, null=True)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True)
    column = models.CharField(max_length=255, blank=True, null=True, choices=ColumnTypeChoice)
    label = models.CharField(max_length=255, null=True)
    position = models.IntegerField()
    default = models.BooleanField(default=False)
    required = models.BooleanField(default = False)
    hide = models.BooleanField(default = False)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, blank=True, null=True, choices=StatusChoice)
    
    def __str__(self):
        return self.label
    
