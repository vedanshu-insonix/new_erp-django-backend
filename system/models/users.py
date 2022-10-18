from django.db import models
from sales.models.address import Address
from ..models.common import BaseContent, Language
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
  
class UserAddress(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserAddress')
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class UserOthers(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserOther')
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(max_length= 2, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user


class UserRoles(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserRoles')
    role = models.ForeignKey('Role', on_delete= models.CASCADE, null=True)
    conditions = models.CharField(max_length = 255, null= True, blank = True)
    commission = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    
""" get user langauge"""
def get_current_user_language(user):
    try:
        get_address = UserAddress.objects.filter(user = user.id, address__type = "user").first()
        address_details = Address.objects.filter(id = get_address.address.id).first()
        if address_details:
            language = address_details.language
        else:
            language = "US English"
            
        return language
    except Exception as e:
        raise ValueError(e)


