from django.db import models
from system.models.common import BaseContent
from system.utils import LocationChoice, StatusChoice
from phonenumber_field.modelfields import PhoneNumberField
from system.models.common import *


class Addresses(BaseContent):
    address_type = models.CharField(max_length=255, null=True, blank=True) #choice
    address_location_type = models.CharField(max_length=255, null=True, blank=True) #choice
    default = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    address3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True) 
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    address_description = models.CharField(max_length=255, null=True, blank=True) #choice
    internal_comments= models.TextField(blank=True, null=True)
    internal_warning = models.TextField(blank=True, null=True)
    external_comments = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=2, blank=True, null=True)
    email = models.EmailField(('email'),max_length=255,null=True,blank=True)
    telephone = PhoneNumberField(null=True, blank=True)
    telephone_type = models.CharField(max_length=255, null=True, blank=True) #choice
    other_communication = models.CharField(max_length= 255, null=True, blank=True)
    other_communication_type = models.CharField(max_length=255, null=True, blank=True) #choice
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
    
    
class AddressTag(BaseContent):
    address = models.ForeignKey('Addresses', on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.tag)