from django.db import models
from system.models.common import BaseContent

class Accounts(BaseContent):
    type = models.ForeignKey('system.Choice', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('system.Category', on_delete = models.CASCADE, null = True, blank = True)
    code = models.CharField(max_length = 255, null = True, blank = True)
    system_name = models.CharField(max_length = 255, null = True, blank = True)
    system_description = models.TextField(null = True, blank = True)
    initial_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    credits = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    debits = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    current_balance = models.DecimalField(max_digits=30,decimal_places=2,blank=True,default=0.0)
    opening_date = models.DateTimeField(null=True,blank=True)
    closing_date = models.DateTimeField(null=True,blank=True)



