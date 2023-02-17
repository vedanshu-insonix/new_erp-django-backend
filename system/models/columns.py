from django.db import models
from .common import BaseContent
from system.utils import ColumnVisibilityChoice
    
class Column(BaseContent):
    clist = models.ForeignKey('List', on_delete=models.CASCADE,null=True, blank=True)
    column = models.CharField(max_length=255, null=True, blank=True)
    dataset = models.ForeignKey('system.Table',on_delete=models.CASCADE,null=True, blank=True)
    data = models.ForeignKey('system.Data',on_delete=models.CASCADE,null=True, blank=True)
    #description =models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    visibility = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):
        return self.column
    
