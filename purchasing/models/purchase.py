from django.db import models
from django.forms import CharField
from system.models.common import BaseContent
from system.utils import EntityChoice, ShippingTermsChoice, StatusChoice
from system.models.common import *

class PurchaseOrder(BaseContent):
    purchase_order_id = models.IntegerField(null=True,blank=True)
    vendor = models.ForeignKey('sales.Vendor', on_delete=models.CASCADE, null=True)
    #contact_address_id = 
    contact_first = models.CharField(max_length = 255, null=True, blank=True)
    contact_last = models.CharField(max_length = 255, null=True, blank=True)
    contact_telephone = models.IntegerField()
    contact_email = models.EmailField('Email', max_length=255,null=True, blank=True)
    #purchase_addr_id =
    purchasing_first = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_last = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_company = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_address_1 = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_address_2 = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_address_3 = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_city = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_state = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_postal_code = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_country = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_telephone = models.CharField(max_length = 255, null=True, blank=True)
    purchasing_email = models.EmailField('Email', max_length=255,null=True, blank=True)
    purchasing_note = models.TextField()
    #shipping_address_id = 
    shipping_first = models.CharField(max_length = 255, null=True, blank=True)
    shipping_last = models.CharField(max_length = 255, null=True, blank=True)
    shipping_company = models.CharField(max_length = 255, null=True, blank=True)
    shipping_address_1 = models.CharField(max_length = 255, null=True, blank=True)
    shipping_address_2 = models.CharField(max_length = 255, null=True, blank=True)
    shipping_address_3 = models.CharField(max_length = 255, null=True, blank=True)
    shipping_city = models.CharField(max_length = 255, null=True, blank=True)
    shipping_state = models.CharField(max_length = 255, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length = 255, null=True, blank=True)
    shipping_country = models.CharField(max_length = 255, null=True, blank=True)
    shipping_telephone = models.CharField(max_length = 255, null=True, blank=True)
    shipping_email = models.EmailField('Email', max_length=255,null=True, blank=True)
    shipping_note = models.TextField(null=True,blank=True)
    date = models.DateTimeField()
    reference = models.CharField(max_length = 255, null=True, blank=True)
    # payment_terms_choices_id = 
    shipping_terms_choices_id = models.CharField(max_length=1, choices=ShippingTermsChoice, null=True, blank=True)
    # Priority = 
    # authorized_by_id = 
    stage_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(auto_now_add=True)
    status_choices_id = models.CharField(max_length=1, choices=StatusChoice, null=True, blank=True)

class PurchaseOrderLines(BaseContent):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_product = models.ForeignKey('sales.VendorProducts', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_stock_number = models.CharField(max_length = 255, null=True, blank=True)
    vendor_product_name = models.CharField(max_length = 255, null=True, blank=True)
    vendor_product_description = models.TextField(null=True,blank=True)
    vendor_list_price = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    vendor_multiplier = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    #vendor_uom = datatype of field is not specified
    ordered = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    canceled = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    confirmed = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    shipped = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    invoiced = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    #route_id = FKey
    #via_choice_id = Fkey
    date = models.DateTimeField()
    sequence = models.IntegerField()
    comment = models.TextField(null=True,blank=True)
    product = models.TextField(null=True,blank=True)
    delivery_id = models.ForeignKey('warehouse.Deliveries', on_delete=models.SET_NULL, null=True, blank=True)
    #bill_id = Fkey
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)


class Disbursment(BaseContent):
    amount = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    currency_id = models.ForeignKey('system.Currency', on_delete=models.SET_NULL, null=True, blank=True)
    disbursment_for = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(null=True,blank=True)
    #sales_credit = models.ForeignKey('sales.Credit', on_delete=models.SET_NULL, null=True, blank=True)
    #vendor_bill = models.ForeignKey('sales.VendorBill', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice, null=True, blank=True)
    stage_started =  models.DateTimeField(null=True, blank=True)

