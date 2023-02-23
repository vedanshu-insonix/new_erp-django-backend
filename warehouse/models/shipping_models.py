from random import choices
from django.db import models
from system.models.common import BaseContent
from system.models.common import *
from system.utils import *


class Deliveries(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    date_received = models.DateTimeField(null=True, blank=True)
    purchase_order = models.ForeignKey('purchasing.PurchaseOrder', on_delete=models.SET_NULL, null=True, blank=True)
    #sales_return = models.ForeignKey('sales.Returns', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(max_length= 2, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)

class DeliveryLines(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    delivery = models.ForeignKey('Deliveries', on_delete=models.SET_NULL, null=True, blank=True)

class Shipments(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    pass

class ContainerTypes(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    container = models.CharField(max_length=100, null=True, blank=True)
    dimension_1 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    dimension_2 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    dimension_3 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    weight = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    surcharge = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_choice_id = models.CharField(max_length=1, choices=StatusChoice, null=True, blank=True)

class Containers(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    type = models.ForeignKey('ContainerTypes', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('warehouse.Locations', on_delete=models.SET_NULL, null=True, blank=True)
    #function = datatype not mentioned
    form = models.ForeignKey('system.Form', on_delete=models.SET_NULL, null=True, blank=True)
    #form_id = models.IntegerField()
    #for = datatype not defined
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_id = models.CharField(max_length=1, choices=StatusChoice, null=True, blank=True)

class Contents(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    container = models.ForeignKey('warehouse.Containers', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('warehouse.Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True) #quantity of product in BOM