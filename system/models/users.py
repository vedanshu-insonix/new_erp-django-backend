from itertools import chain
from django.db import models
from sales.models.address import Address
from system.models.common import BaseContent
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
  
class UserAddress(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserAddress')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user

class UserOthers(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserOther')
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(max_length= 2, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user



