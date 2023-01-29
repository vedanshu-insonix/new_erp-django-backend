from django.db import models
from system.models.common import *

class Product(BaseContent):
    template = models.ForeignKey('self', on_delete = models.SET_NULL, null=True, blank=True)
    template_name = models.CharField(max_length = 255, null=True, blank=True)
    template_subname = models.CharField(max_length = 255, null=True, blank=True)
    template_description = models.TextField(null=True, blank=True)
    template_variant = models.CharField(max_length = 255, null=True, blank=True)#FKEY Lookup Field
    template_variant_name = models.CharField(max_length = 255, null=True, blank=True)
    stock_number = models.CharField(max_length = 255, null=True, blank=True)
    variant_name = models.CharField(max_length = 255, null=True, blank=True)
    cart_line_description = models.TextField(null=True, blank=True)
    sales_line_description = models.TextField(null=True, blank=True)
    list_price = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    # selling_unit = models.ForeignKey('UOM', on_delete = models.SET_NULL, null=True, blank=True)
    stocking_unit = models.ForeignKey('UOM', on_delete = models.SET_NULL, null=True, blank=True)
    product_type = models.ForeignKey('system.Configuration', on_delete = models.SET_NULL, null=True, blank=True)
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
    status_choices = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)

class Bom(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    template = models.ForeignKey('Journal_Template', on_delete = models.SET_NULL, null=True, blank=True)
    resulting_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    bom_description = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    BOMTypeChoice =(("1","Assembly"),("2","Kit"),
                    ("3","Set"),("4","Bundle")
                    )
    bom_type = models.CharField(max_length=255, null=True, blank=True, choices=BOMTypeChoice)
    version = models.IntegerField(null=True, blank=True)

class Components(BaseContent):
    bom = models.ForeignKey('Bom', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    uom = models.ForeignKey('UOM', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    template = models.ForeignKey('Journal_Template', on_delete = models.SET_NULL, null=True, blank=True)

class Characteristics(BaseContent):
    template = models.ForeignKey('Journal_Template', on_delete = models.SET_NULL, null=True, blank=True)
    Characteristics = models.CharField(max_length=255, null=True, blank=True) # FKEY Lookup Field
    before = models.CharField(max_length=255, null=True, blank=True)
    after = models.CharField(max_length=255, null=True, blank=True)

class Value(BaseContent):
    value = models.CharField(max_length=255, null=True, blank=True) # FKEY Lookup Field
    attribute = models.ForeignKey('Attributes', on_delete=models.SET_NULL, null=True, blank=True)

class Product_Values(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    value = models.ForeignKey('Value', on_delete=models.SET_NULL, null=True, blank=True)

class ProductCategory(BaseContent):
    usage = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('system.Category', on_delete = models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True) # parent_id
    has_children = models.BooleanField(default = False)
    sequence = models.CharField(max_length=255, null=True, blank=True)

class Equivalents(BaseContent):
    company = models.ForeignKey('system.Entity', on_delete=models.SET_NULL, null=True, blank=True)
    company_product = models.ForeignKey('system.EntityProducts', on_delete=models.SET_NULL, null=True, blank=True)
    company_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    #company_uom = data type not defined
    vendor_id = models.ForeignKey('sales.Vendors', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_product = models.ForeignKey('sales.VendorProducts', on_delete=models.SET_NULL, null=True, blank=True)
    vendor_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    #vendor_uom = data type not defined

class Locations(BaseContent):
    parent_location = models.ForeignKey('Locations', on_delete=models.SET_NULL, null=True, blank=True)
    locations_name = models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100,null=True,blank=True)
    loc_address = models.ForeignKey('sales.Addresses', on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(null=True,blank=True)
    LocationTypeChoice =(("company","Companies"),("customer","Customers"),
                        ("vendor","Vendors"))
    loc_type=models.CharField(max_length=255, null=True, blank=True, choices=LocationTypeChoice)
    stock=models.BooleanField(default = False)
    packing=models.BooleanField(default = False)
    manufacturing=models.BooleanField(default = False)
    shipping=models.BooleanField(default = False)
    receiving=models.BooleanField(default = False)
    inspection=models.BooleanField(default = False)
    transit=models.BooleanField(default = False)
    scrap=models.BooleanField(default = False)
    stage=models.ForeignKey('system.Stage', on_delete = models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length = 255, null=True, blank=True)

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
    mini_quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    comment = models.TextField(null=True,blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status_choices = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)

class UOM(BaseContent):
    uom_category = models.CharField(max_length=100,null=True,blank=True)#choice field
    name = models.CharField(max_length=100,null=True,blank=True)
    abbreviation = models.CharField(max_length=100,null=True,blank=True)
    unit = models.TextField(null=True,blank=True)
    reference = models.TextField(null=True,blank=True)
    rounding = models.TextField(null=True,blank=True)

class ProductLine(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    reserve = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    ship = models.IntegerField(null=True, blank=True)
    route = models.ForeignKey('warehouse.Routes', on_delete=models.SET_NULL, null=True, blank=True)
    via = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    unit = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    discount = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    net = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)