from django.db import models
from system.models.common import BaseContent

class SalesQuotations(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    quotation_id = models.CharField(max_length = 10, unique=True)
    customer = models.ForeignKey('Customers', on_delete = models.CASCADE)
    contact_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_contact_address")
    contact_first = models.CharField(max_length = 255, null = True, blank = True)
    contact_last = models.CharField(max_length = 255, null = True, blank = True)
    contact_telephone = models.CharField(max_length = 255, null = True, blank = True)
    contact_email = models.CharField(max_length = 255, null = True, blank = True)
    billing_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_billing_address")
    billing_first = models.CharField(max_length = 255, null = True, blank = True)
    billing_last = models.CharField(max_length = 255, null = True, blank = True)
    billing_company = models.CharField(max_length = 255, null = True, blank = True)
    billing_address_1 = models.CharField(max_length = 255, null = True, blank = True)
    billling_address_2 = models.CharField(max_length = 255, null = True, blank = True)
    billing_address_3 = models.CharField(max_length = 255, null = True, blank = True)
    billing_city = models.CharField(max_length = 255, null = True, blank = True)
    billing_state = models.ForeignKey('system.State', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_billing_state")
    billing_postal_code = models.CharField(max_length = 255, null = True, blank = True)
    billing_country = models.ForeignKey('system.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_blling_country")
    billing_telephone = models.CharField(max_length = 255, null = True, blank = True)
    billing_email = models.CharField(max_length = 255, null = True, blank = True)
    billing_note = models.TextField(null = True, blank = True)
    shipping_address = models.ForeignKey('Addresses', on_delete = models.SET_NULL, null = True, blank = True, related_name="%(class)s_shipping_address")
    shipping_first = models.CharField(max_length = 255, null = True, blank = True)
    shipping_last = models.CharField(max_length = 255, null = True, blank = True)
    shipping_company = models.CharField(max_length = 255, null = True, blank = True)
    shipping_address_1 = models.CharField(max_length = 255, null = True, blank = True)
    shipping_address_2 = models.CharField(max_length = 255, null = True, blank = True)
    shipping_address_3 = models.CharField(max_length = 255, null = True, blank = True)
    shipping_city = models.CharField(max_length = 255, null = True, blank = True)
    shipping_state = models.ForeignKey('system.State', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_shipping_state")
    shipping_postal_code = models.CharField(max_length = 255, null = True, blank = True)
    shipping_country = models.ForeignKey('system.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_shipping_country")
    shipping_telephone = models.CharField(max_length = 255, null = True, blank = True)
    shipping_email = models.CharField(max_length = 255, null = True, blank = True)
    shipping_note = models.TextField(null = True, blank = True)
    quotation_date = models.DateTimeField(null = True, blank = True)
    reference = models.CharField(max_length = 255, null = True, blank = True)
    payment_terms = models.CharField(max_length = 255, null = True, blank = True)
    shipping_terms = models.CharField(max_length = 255, null = True, blank = True)
    priority = models.CharField(max_length = 255, null = True, blank = True)
    accepted_amount = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    accepted_currency = models.ForeignKey('system.Currency', on_delete = models.SET_NULL, null= True, blank = True)
    merchandise = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    other = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    tax = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    shipping = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    total = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    quotation_stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.quotation_id

class SalesQuotationLines(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    quotation_id = models.ForeignKey('system.Currency', on_delete = models.SET_NULL, null= True, blank = True)
    stock_id = models.CharField(max_length = 255, null = True, blank = True)
    #stock_number = 
    product_name = models.CharField(max_length = 255, null = True, blank = True)
    #description = 
    list_price = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    multiplier = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    #uom = FKEY
    quantity = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    route = models.ForeignKey('warehouse.Routes', on_delete = models.SET_NULL, null= True, blank = True)
    #via_choice = 
    date = models.DateTimeField(null=True,blank=True)
    #bundle_line_id = 
    #order_id = 
    #sequence = 
    comment = models.TextField(null = True, blank = True)
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    #status_choices_id = 