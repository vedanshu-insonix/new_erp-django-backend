from django.db import models
from system.models.common import BaseContent
from system.utils import LocationChoice
from phonenumber_field.modelfields import PhoneNumberField
from system.models.common import *

class Address(BaseContent):
    type = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    person = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    address3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    location = models.CharField(max_length=1, choices=LocationChoice, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    telephone = PhoneNumberField(null=True, blank=True)
    telephone_type = models.CharField(max_length= 255, null=True, blank=True)
    email = models.EmailField(('email'),max_length=255,null=True,blank=True)
    other_communication = models.CharField(max_length= 255, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True)
    used = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, blank=True, null=True)
    warning = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.type
    
    
class Source(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

    
    
