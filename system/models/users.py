from itertools import chain
from django.db import models
from system.models.common import BaseContent
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class UserPhone(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    telephone = PhoneNumberField()
    other_communication = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.telephone
    
class UserAddress(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    address1 = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255, null=True)
    address3 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.CharField(max_length= 6, null=True, blank=True)
    
    def __str__(self):
        return self.user

class UserOthers(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    tags = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, blank=True)
    icon = models.CharField(max_length= 2, null=True, blank=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user
    


