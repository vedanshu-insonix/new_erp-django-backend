from django.db import models
from system.models.common import BaseContent
from django.contrib.auth.models import User
from sales.models.address import Addresses

class Company(BaseContent):
    name = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
    

class CompanyUser(BaseContent):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.user
    
class CompanyAddress(BaseContent):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    address = models.OneToOneField(Addresses, on_delete=models.CASCADE, null=True, unique=True)
    def __str__(self):
        return self.address
    
class CompanyProducts(BaseContent):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE, null=True, blank=True)