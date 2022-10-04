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
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name="%(class)s_created_by")
    class Meta:
        abstract = True

class Button(BaseContent):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    function = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
   
class Currency(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    code = models.CharField(max_length=3, null=True, unique=True)
    symbol = models.CharField(max_length=1, null=True, unique=True)
    current_rate = models.DecimalField(max_digits= 30, decimal_places=2,null= True, blank=True)
    updated = models.DateTimeField(null=True, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Countries"
     
class Tag(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Language(BaseContent): 
    name = models.CharField(max_length=255, null=True, unique=True)
    date_format = models.CharField(max_length=255, choices=DateFormatChoices, null=True, blank=True)
    time_format = models.CharField(max_length=255, choices=TimeFormatChoice, null=True, blank=True)
    symbol_position = models.IntegerField(null=True, unique=True)
    thousands_separator = models.CharField(max_length=255, null=True, unique=True)
    fraction_separator = models.CharField(max_length=255, null=True, unique=True)
    decimal_places = models.IntegerField(null=True, unique=True)
    
    def __str__(self):
        return self.name
    
class Country(BaseContent):
    name = models.CharField(max_length=255, null=True,unique=True)
    abbreviation = models.CharField(max_length=255, null=True, unique=True)
    currency = models.ForeignKey('Currency', on_delete= models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class State(BaseContent):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    abbreviation = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name

class Stage(BaseContent):
    application = models.CharField(max_length=255, null=True, unique=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    stage = models.CharField(max_length=255, null=True, blank=True)
    warning_interval = models.DateTimeField(null=True, blank=True)
    urgent_interval = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.stage
    
class Configuration(BaseContent):
    application = models.ForeignKey('App', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    current_integer = models.IntegerField(null=True, blank=True)
    default_integer = models.IntegerField(null=True, blank=True)
    current_decimal = models.DecimalField(max_digits=30, decimal_places =2, null=True, blank=True)
    default_decimal = models.DecimalField(max_digits=30, decimal_places =2, null=True, blank=True)
    current_char = models.CharField(max_length=255, null=True, blank=True)
    default_char = models.CharField(max_length=255, null=True, blank=True)
    current_color = models.CharField(max_length=255, null=True, blank=True)
    default_color = models.CharField(max_length=255, null=True, blank=True)
    current_boolean = models.BooleanField(default=False)
    default_boolean = models.BooleanField(default=False)
    current_interval = models.DateTimeField(null=True, blank=True)
    default_interval = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.application
    

class Territories(BaseContent):
    use = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Territories"
        verbose_name_plural = "Territories"
    
class Choice(BaseContent):
    application = models.ForeignKey('App', on_delete=models.CASCADE, null=True, blank=True)
    field = models.ForeignKey('Field', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.field
    
class Field(BaseContent):
    application = models.ForeignKey('App', on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    panel = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Menu(BaseContent):
    menu_category = models.CharField(max_length = 255, null=True, blank =True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

class Form(BaseContent):
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

class FormList(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    primary = models.BooleanField(default = False)
    sequence = models.IntegerField(null=True, blank=True)

class FormData(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    data = models.CharField(max_length=255, null=True, blank=True)
    panel = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

class List(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True , blank=True)
    
    def __str__(self):
        return str(self.id)

class Help(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    published = models.BooleanField(default = True)
    
    def __str__(self):
        return self.title
    
class Category(BaseContent):
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tile(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    list_view = models.CharField(max_length = 255, null=True, blank=True)
    search_criteria = models.CharField(max_length = 255, null=True, blank=True)
    