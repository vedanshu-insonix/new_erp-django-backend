from django.db import models
from system.models.common import BaseContent
# Create your models here.

class Customers(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    parent_id = models.ForeignKey('Customers', on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_entity")
    customer = models.CharField(max_length=100,null=True,blank=True)
    shipping_terms = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_terms")
    ship_via = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_method")
    customer_source = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_source")
    payment_terms = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_terms")
    payment_method = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_method")
    currency = models.ForeignKey('system.Currency', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_currency")
    free_freight_minimum = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    issue_statements = models.BooleanField(default=False)
    require_pos = models.BooleanField(default=False)
    credit_limit = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    account_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    current_orders = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    authorised_card = models.DecimalField(max_digits=30,decimal_places=2,blank=True, default=0.0)
    credit_available = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    overdue = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    average_pay_days = models.IntegerField(null=True,blank=True)
    last_credit_review = models.DateField(blank=True, null=True)
    credit_hold = models.BooleanField(default=False)
    customer_receivable_account = models.CharField(max_length = 255, null = True, blank = True) #later will convert into foreign key
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="status")
    used = models.DateTimeField(null=True, blank=True)
    
    # def __str__(self):
    #     return self.entity
    
class CustomerAddress(BaseContent):
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, null=True)
    address = models.OneToOneField('Addresses', on_delete=models.CASCADE, null=True, unique=True)
    
