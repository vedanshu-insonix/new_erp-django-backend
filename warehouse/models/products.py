from django.db import models
from system.models.common import BaseContent
from system.models.common import *


class Template(BaseContent):
    pass

class Product(BaseContent):
    template = models.ForeignKey('Template', on_delete = models.SET_NULL, null=True, blank=True)
    is_template = models.BooleanField(default=False)
    is_product = models.BooleanField(default=False)
    sales_description = models.TextField(null=True, blank=True)
    website_description = models.TextField(null=True, blank=True)
    list_price = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    # selling_unit = models.ForeignKey('UOM', on_delete = models.SET_NULL, null=True, blank=True)
    # stocking_unit = models.ForeignKey('UOM', on_delete = models.SET_NULL, null=True, blank=True)
    product_type = models.CharField(max_length=255, null=True, blank =True)
    version = models.CharField(max_length = 100, null=True, blank=True)
    warranty = models.IntegerField(null=True, blank=True)
    tracking = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    dimension_1 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    dimension_2 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    dimension_3 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    additional_dimension_3 = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    cross_section = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    volume = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    packing_category_choice = models.CharField(max_length=255, null=True, blank=True)
    dedicated_container_choice = models.CharField(max_length=255, null=True, blank=True)
    quantity_in_container = models.FloatField(null=True, blank=True)
    item_surcharge = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    line_surcharge = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    unit_weight = models.FloatField(null=True, blank=True)
    additional_weight = models.FloatField(null=True, blank=True)
    unit_time = models.IntegerField(null=True, blank=True)
    additional_time = models.IntegerField(null=True, blank=True)
    truckload_quantity = models.FloatField(null=True, blank=True)
    container_quantity = models.FloatField(null=True, blank=True)
    shipping_delay = models.DateTimeField(null=True, blank=True)
    sales_warning = models.TextField(null=True, blank=True)
    sales_comments = models.TextField(null=True, blank=True)
    shipping_warning = models.TextField(null=True, blank=True)
    shipping_comments = models.TextField(null=True, blank=True)
    receiving_warning = models.TextField(null=True, blank=True)
    receiving_comments = models.TextField(null=True, blank=True)
    purchasing_warning = models.TextField(null=True, blank=True)
    purchasing_comments = models.TextField(null=True, blank=True)
    accounting_warning = models.TextField(null=True, blank=True)
    accounting_comments = models.TextField(null=True, blank=True)
    accounting_comments = models.TextField(null=True, blank=True)
    # income_account = models.ForeignKey('ChartOfAccounts', on_delete = models.SET_NULL, null=True, blank=True)
    # expense_account = models.ForeignKey('ChartOfAccounts', on_delete = models.SET_NULL, null=True, blank=True)
    # price_difference_account = models.ForeignKey('ChartOfAccounts', on_delete = models.SET_NULL, null=True, blank=True)
    deferred_revenue_type = models.CharField(max_length=255, null=True, blank=True)
    asset_type = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    
    
class Bom(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    template = models.ForeignKey('Template', on_delete = models.SET_NULL, null=True, blank=True)
    resulting_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    #bom_type_choice_id = 
    version = models.IntegerField(null=True, blank=True)

class Components(BaseContent):
    bom = models.ForeignKey('Bom', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)

class Characteristics(BaseContent):
    template_id = models.ForeignKey('Template', on_delete = models.SET_NULL, null=True, blank=True)
    #Characteristics = (lookup)
    before = models.CharField(max_length=255, null=True, blank=True)
    after = models.CharField(max_length=255, null=True, blank=True)

class Value(BaseContent):
    Characteristics_id = models.ForeignKey('Characteristics', on_delete = models.SET_NULL, null=True, blank=True)
    #value_choices_id = (lookup)

class ProductCategory(BaseContent):
    usage = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('system.Category', on_delete = models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True) # parent_id
    has_children = models.BooleanField()
    sequence = models.CharField(max_length=255, null=True, blank=True)

class Equivalents(BaseContent):
    company = models.ForeignKey('system.Company', on_delete=models.SET_NULL, null=True, blank=True)
    company_product = models.ForeignKey('system.CompanyProducts', on_delete=models.SET_NULL, null=True, blank=True)
    company_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    #company_uom = data type not defined
    vendor_id = models.ForeignKey('sales.Vendor', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_product = models.ForeignKey('sales.VendorProducts', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    #vendor_uom = data type not defined

class Locations(BaseContent):
    parent_location = models.ForeignKey('Locations', on_delete=models.SET_NULL, null=True, blank=True)
    locations_name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)
    loc_address = models.ForeignKey('sales.Address', on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(null=True,blank=True)
    function_choice = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)

class ProductCounts(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    locations = models.ForeignKey('Locations', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()
    counted = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    discrepancy = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    comment = models.TextField(null=True,blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_choices = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)

class ProductLocations(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    locations = models.ForeignKey('Locations', on_delete=models.SET_NULL, null=True, blank=True)
    current_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    max_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    mimi_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    comment = models.TextField(null=True,blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_choices = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)