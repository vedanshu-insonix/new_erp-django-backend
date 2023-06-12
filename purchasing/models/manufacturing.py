from django.db import models
from system.models.common import *

class Manufacturingorders(BaseStatus):
    id = models.CharField(max_length=255, primary_key=True, editable=False)

class Manufacturingorderlines(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    product = models.ForeignKey('warehouse.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    bom = models.ForeignKey('warehouse.BOM', on_delete=models.SET_NULL, null=True, blank=True)