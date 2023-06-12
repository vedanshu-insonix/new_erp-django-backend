from django.db import models
from sales.models.address import Addresses
from ..models.common import BaseContent, Language, BaseStatus
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# class UserAddress(BaseContent):
#     user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserAddress')
#     address = models.OneToOneField(Addresses, on_delete=models.SET_NULL, null=True, blank=True)
#     def __str__(self):
#         return str(self.id)

# class UserOthers(BaseStatus):
#     user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserOther')
#     used = models.DateTimeField(null=True, blank=True)
    
#     def __str__(self):
#         return self.user
    
class UserRoles(BaseContent):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True, related_name='UserRoles')
    role = models.ForeignKey('Role', on_delete= models.CASCADE, null=True)
    conditions = models.CharField(max_length = 255, null= True, blank = True)
    commission = models.DecimalField(max_digits=30,decimal_places=2,default=0.0)
    
""" get user langauge"""
def get_current_user_language(user):
    try:
        getAddr = Addresses.objects.filter(company__user = user.id).first()
        language = "English (US)"
        if getAddr:
            language = getAddr.language.system_name
            print(language)
                
        return language
    except Exception as e:
        raise ValueError(e)
    # try:
    #     get_address = UserAddress.objects.filter(user = user.id, address__address_type = "user").first()
    #     language = "English (US)"
    #     if get_address:
    #         address_details = Addresses.objects.filter(id = get_address.address.id).first()
    #         if address_details:
    #             language = address_details.language.system_name
                
    #     return language
    # except Exception as e:
    #     raise ValueError(e)


