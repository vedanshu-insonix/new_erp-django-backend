from django.db import models
from system.models.common import *

class Operations(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    route=models.ForeignKey('warehouse.Routes', on_delete = models.SET_NULL, null=True, blank=True)
    name=models.CharField(max_length = 255, null=True, blank=True)
    origin_description=models.CharField(max_length=255, null=True, blank=True)
    destination_description=models.CharField(max_length=255, null=True, blank=True)
    stage=models.ForeignKey('system.Stage', on_delete = models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length = 255, null=True, blank=True)

class Transfers(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    transfer_type = models.CharField(max_length = 255, null=True, blank=True)
    transfer_id = models.CharField(max_length = 255, null=True, blank=True)
    order_id = models.CharField(max_length = 255, null=True, blank=True)
    via = models.CharField(max_length = 255, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    origin=models.ForeignKey('warehouse.Locations', on_delete = models.SET_NULL, null=True, blank=True, related_name='origin')
    destination=models.ForeignKey('warehouse.Locations', on_delete = models.SET_NULL, null=True, blank=True, related_name='destination') 
    stage=models.ForeignKey('system.Stage', on_delete = models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length = 255, null=True, blank=True)