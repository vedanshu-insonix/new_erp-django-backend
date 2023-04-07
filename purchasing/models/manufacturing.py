from django.db import models
from system.models.common import *

class Manufacturingorders(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)

class Manufacturingorderlines(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    product = models.ForeignKey('warehouse.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    bom = models.ForeignKey('warehouse.BOM', on_delete=models.SET_NULL, null=True, blank=True)