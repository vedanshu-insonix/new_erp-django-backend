from django.db import models
from .common import BaseContent

class DataTable(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)
    link_source = models.CharField(max_length=255, null=True, blank=True)

class Data(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    data_source=models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True, blank=True)
    system_name= models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    display_data = models.CharField(max_length=225, null=True, blank=True)
    field_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)

class DataSelector(BaseContent):
    selector = models.ForeignKey('Selectors', on_delete=models.SET_NULL, null=True, blank=True)
    data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)

class DataRequirements(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.SET_NULL, null=True, blank=True)
    data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    requirement = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
