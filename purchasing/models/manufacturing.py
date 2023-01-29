from django.db import models
from system.models.common import *

class Manufacturing_orders(BaseContent):
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)

class Manufacturing_order_lines(BaseContent):
    product = models.ForeignKey('warehouse.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    bom = models.ForeignKey('warehouse.BOM', on_delete=models.SET_NULL, null=True, blank=True)