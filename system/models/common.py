from re import L
from statistics import mode
from django.db import models
from system.utils import DateFormatChoices, TimeFormatChoice
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
    code = models.CharField(max_length=3, null=True, unique=True)
    symbol = models.CharField(max_length=1, null=True, unique=True)
    current_rate = models.DecimalField(max_digits= 30, decimal_places=2,null= True, blank=True)
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
    direction = models.CharField(max_length=255, null=True, unique=True)
    date_format = models.CharField(max_length=255, choices=DateFormatChoices, null=True, blank=True)
    time_format = models.CharField(max_length=255, choices=TimeFormatChoice, null=True, blank=True)
    currency_symbol_position = models.IntegerField(null=True, unique=True)
    thousands_separator = models.IntegerField(null=True, unique=True)
    decimal_places = models.IntegerField(null=True, unique=True)
    decimal_separator = models.IntegerField(null=True, unique=True)
    
    def __str__(self):
        return self.name
    
class Country(BaseContent):
    name = models.CharField(max_length=255, null=True,unique=True)
    code = models.CharField(max_length=255, null=True, unique=True)
    currency = models.ForeignKey('Currency', on_delete= models.SET_NULL, null=True, blank=True)
    
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
    
