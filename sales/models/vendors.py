from django.db import models
from system.models.common import BaseContent
from system.utils import EntityChoice, StatusChoice
from system.models.common import *
# Create your models here.

class Vendors(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    parent_id = models.ForeignKey('Vendors', on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.CharField(max_length=255, choices=EntityChoice)
    vendor = models.CharField(max_length=100,null=True,blank=True)
    shipping_terms = models.CharField(max_length=255, null=True, blank=True) #choice
    ship_via = models.CharField(max_length=255, null=True, blank=True) #choice
    payment_terms = models.CharField(max_length=255, null=True, blank=True) #choice
    payment_method = models.CharField(max_length=255, null=True, blank=True) #choice
    purchasing_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    free_freight_minimum = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    require_pos = models.BooleanField(default=False)
    require_rfq = models.BooleanField(default=False)
    minimum_orders = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    credit_limit = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    account_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    current_orders = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    credit_available = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    overdue_bills = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    average_pay_days = models.IntegerField(null=True,blank=True)
    last_credit_review = models.DateField(blank=True, null=True)
    credit_hold = models.BooleanField(default=False)
    vendor_payable_account = models.CharField(max_length = 255, null = True, blank = True) #later will convert into foreign key
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.entity
    
class VendorAddress(BaseContent):
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE, null=True)
    address = models.OneToOneField('Addresses', on_delete=models.CASCADE, null=True, unique=True)
    def __str__(self):
        return str(self.id)

class VendorProducts(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    stock_number = models.CharField(max_length=3,null=True,blank=True)
    vendor_product_description = models.CharField(max_length=255,null=True,blank=True)
    list_price = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    uom = models.ForeignKey('warehouse.UOM', on_delete = models.SET_NULL, null = True, blank = True)
    version = models.CharField(max_length=255,null=True,blank=True)
    warranty = models.IntegerField()
    barcode = models.CharField(max_length=255,null=True,blank=True)
    dimension_1 = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    dimension_2 = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    dimension_3 = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0) 
    additional_dimension_3 = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    cross_section = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    volume = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    packing_category = models.CharField(max_length=255,null=True,blank=True)
    dedicated_container = models.CharField(max_length=255,null=True,blank=True)
    quantity_in_container = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    item_surcharge = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    line_surcharge = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    unit_weight = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    additional_weight = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    truckload_quantity = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    container_quantity = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    nmfc_code_id = models.ForeignKey('NMFC', on_delete=models.SET_NULL, null=True, blank=True)
    hts_code_id = models.ForeignKey('CustomsClassifications', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_delay = models.DateTimeField(null=True, blank= True)
    shipping_warning = models.TextField(null=True,blank=True)
    shipping_comments = models.TextField(null=True,blank=True)
    receiving_warning = models.TextField(null=True,blank=True)
    receiving_comments = models.TextField(null=True,blank=True)
    purchasing_warning = models.TextField(null=True,blank=True)
    purchasing_comments = models.TextField(null=True,blank=True)
    asset_type = models.TextField(null=True,blank=True) # datatype not defined
    stage_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, null=True, blank=True)

class CustomsClassifications(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    hts_code = models.CharField(max_length = 255, null = True, blank = True)
    hts_code_description = models.TextField(null = True, blank = True)
    hts_duty = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    
class NMFC(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    pass

class VendorPrices(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE, null=True)
    vendor_product_id = models.ForeignKey('VendorProducts', on_delete=models.CASCADE, null=True)
    base_price = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    #currency = Fkey?
    #uom = FKey
    multiplier = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    minimum = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    minimum_in_category = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    minimum_in_order = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    minimum_order_total = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    multiple = models.DecimalField( max_digits= 30, decimal_places=2,blank=True,default=0.0)
    beginning = models.DateTimeField
    ending = models.DateTimeField()
    rounding_precision = models.IntegerField()
    preferred = models.TextField(null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    stage_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_choice_id = models.CharField(max_length=1, choices=StatusChoice, null=True, blank=True)