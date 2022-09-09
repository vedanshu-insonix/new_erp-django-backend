from django.db import models
from system.models.common import BaseContent
from django.contrib.auth.models import User

class Company(BaseContent):
    name = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class CompanyUser(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.user
    
