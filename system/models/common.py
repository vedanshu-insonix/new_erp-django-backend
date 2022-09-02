from re import L
from statistics import mode
from django.db import models
from system.utils import ColumnTypeChoice, StatusChoice	
from django.contrib.auth.models import User

# Create your models here.
# Base class for all models
class BaseContent(models.Model):
    """
        Captures BaseContent as created On and modified On and active field.
        common field accessed for the following classes.
    """
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ShipVia(BaseContent):
    name =  models.CharField(max_length=255, null=True, unique=True)
    def __str__(self):
        return self.name
    

class Currency(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    code = models.CharField(max_length=255, null=True, unique=True)
    
    def __str__(self):
        return self.name
  
class PaymentTerm(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    term = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class PaymentMethod(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    
    def __str__(self):
        return self.name
    
class Tag(BaseContent):
    title = models.CharField(max_length=255, null=True, unique=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Language(BaseContent): 
    name = models.CharField(max_length=255, null=True, unique=True)
    code = models.CharField(max_length=255, null=True, unique=True)
    
    def __str__(self):
        return self.name
    
class Country(BaseContent):
    name = models.CharField(max_length=255, null=True,unique=True)
    code = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.name

class State(BaseContent):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name

class Stage(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
