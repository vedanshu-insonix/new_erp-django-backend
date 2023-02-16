from django.db import models
from system.models.common import BaseContent

class Carts(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    customer = models.ForeignKey('Customers', on_delete = models.CASCADE, null = True, blank = True)
    contact_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_contact_address")
    billing_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_billing_address")
    shipping_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_shipping_address")
    date = models.DateTimeField(null = True, blank = True)
    reference = models.TextField(null = True, blank = True)
    priority = models.CharField(max_length = 255, null = True, blank = True)
    currency = models.ForeignKey('system.Currency', on_delete = models.SET_NULL, null= True, blank = True)
    merchandise = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    other = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    tax = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    shipping = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    total = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

class Cartlines(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    cart = models.ForeignKey('Carts', on_delete = models.CASCADE, null = True, blank = True)
    stock_id = models.CharField(max_length = 255, null = True, blank = True)#FKEY
    stock_number = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null = True, blank = True)
    list_price = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    multiplier = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    uom = models.CharField(max_length = 255, null = True, blank = True)#FKEY
    quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null = True, blank = True)
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)