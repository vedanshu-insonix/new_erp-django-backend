from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from system.models.common import *


class Addresses(BaseStatus):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    address_type = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_address_type')
    address_location_type = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_address_location_type')
    default = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    address3 = models.CharField(max_length=255, null=True, blank=True)
    address_composite = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey('system.State', on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.ForeignKey('system.Country', on_delete=models.SET_NULL, null=True, blank=True)
    address_description = models.CharField(max_length=255, null=True, blank=True)
    internal_comments= models.TextField(blank=True, null=True)
    internal_warning = models.TextField(blank=True, null=True)
    external_comments = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=2, blank=True, null=True)
    email = models.EmailField(('email'),max_length=255,null=True,blank=True)
    telephone = PhoneNumberField(null=True, blank=True)
    telephone_type = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_telephone_type')
    other_communication = models.CharField(max_length= 255, null=True, blank=True)
    other_communication_type = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_communication_type')
    language = models.ForeignKey('system.Language', on_delete=models.SET_NULL, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True, related_name='addresses')
    customer = models.ForeignKey('Customers', on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_method")
    vendor = models.ForeignKey('Vendors', on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_method")
    company = models.ForeignKey('system.Entity', on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_method")
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
    
    
# class AddressTag(BaseContent):
#     address = models.ForeignKey('Addresses', on_delete=models.CASCADE, null=True)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    
#     def __str__(self):
#         return str(self.tag)