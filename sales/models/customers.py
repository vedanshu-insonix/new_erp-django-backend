from django.db import models
from system.models.common import BaseContent
from system.utils import EntityChoice, ShippingTermsChoice, AddressTypeChoice, StatusChoice
from system.models.common import *
# Create your models here.

class Customer(BaseContent):
    parent_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.CharField(max_length=255, choices=EntityChoice)
    name = models.CharField(max_length=100,null=True,blank=True)
    shipping_terms = models.CharField(max_length=255, null=True, blank=True) #choice
    ship_via = models.CharField(max_length=255, null=True, blank=True) #choice
    source = models.CharField(max_length=255, null=True, blank=True) #choice
    payment_terms = models.CharField(max_length=255, null=True, blank=True) #choice
    payment_method = models.CharField(max_length=255, null=True, blank=True) #choice
    sales_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_currency")
    free_freight_min = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    issue_statements = models.BooleanField(default=False)
    require_pos = models.BooleanField(default=False)
    credit_limit = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    account_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    current_orders = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    authorised_card = models.DecimalField(max_digits=30,decimal_places=2,blank=True, default=0.0)
    credit_avail = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    overdue = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    avg_pay_days = models.IntegerField(null=True,blank=True)
    last_credit_review = models.DateField(blank=True, null=True)
    credit_hold = models.BooleanField(default=False)
    account_receivable = models.DateTimeField(null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    # def __str__(self):
    #     return self.entity
    
class CustomerAddress(BaseContent):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    address = models.OneToOneField('Address', on_delete=models.CASCADE, null=True, unique=True)
    
