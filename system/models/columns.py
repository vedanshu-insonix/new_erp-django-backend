from django.db import models
from .common import BaseContent
    
class Column(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    col_list = models.ForeignKey('List', on_delete=models.SET_NULL, null=True)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    col_table = models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True)
    col_data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True)
    position = models.IntegerField(null=True, blank=True)
    visibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.system_name
    
