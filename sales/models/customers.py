from django.db import models
from system.models.common import BaseContent
from system.utils import EntityChoice, ShippingTermsChoice, AddressTypeChoice
from system.models.common import *
# Create your models here.

class Customer(BaseContent):
    entity = models.CharField(max_length=255, choices=EntityChoice, null=True, blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    parent_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_terms = models.CharField(max_length=255, choices=ShippingTermsChoice, null=True, blank=True)
    ship_via = models.ForeignKey(ShipVia, on_delete=models.SET_NULL, null=True, blank=True)
    payment_terms = models.ForeignKey(PaymentTerm, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    sales_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    issue_statements = models.CharField(max_length= 255, null=True, blank=True)
    free_freight_min = models.CharField(max_length=255, null=True, blank=True)
    require_pos = models.CharField(max_length=255, null=True, blank=True)
    account_receivable = models.DateTimeField(null=True, blank=True)
    credit_limit = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    account_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    current_orders = models.IntegerField(blank=True)
    authorised_card = models.CharField(max_length=255,null=True,blank=True)
    credit_avail = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    overdue = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    avg_pay_days = models.IntegerField(blank=True)
    last_credit_review = models.DateTimeField(blank=True, null=True)
    credit_hold = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class CustomerTag(BaseContent):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.tag


class CustomerAddress(BaseContent):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    primary = models.BooleanField(default=False)
    type = models.CharField(max_length=255, choices=AddressTypeChoice, null=True)
    icon = models.CharField(max_length=2, null=True, blank=True)
    
    def __str__(self):
        return self.address
    


