from email.policy import default
from enum import unique
from django.db import models
from system.utils import DateFormatChoices, TimeFormatChoice
from django.contrib.auth.models import User
from django_countries.fields import CountryField

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
    form = models.ForeignKey('Form', on_delete= models.CASCADE, null = True, blank=True)
    button = models.CharField(max_length=255, null=True, blank=True)
    button_type = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.button
    
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
        verbose_name_plural = "Currencies"
     
class Tag(BaseContent):
    tag = models.CharField(max_length=255, null=True, unique=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.tag
    
class Language(BaseContent): 
    name = models.CharField(max_length=255, null=True, unique=True)
    date_format = models.CharField(max_length=255, choices=DateFormatChoices, null=True, blank=True)
    time_format = models.CharField(max_length=255, choices=TimeFormatChoice, null=True, blank=True)
    symbol_position = models.IntegerField(null=True, blank=True)
    thousands_separator = models.CharField(max_length=255, null=True, blank=True)
    fraction_separator = models.CharField(max_length=255, null=True, blank=True)
    decimal_places = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Country(BaseContent):
    country = CountryField(unique=True)
    telephone = models.CharField(max_length=5, null=True, unique= True)
    currency = models.ForeignKey('Currency', on_delete= models.SET_NULL, null=True)
    
    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class State(BaseContent):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=False, blank=True)
    abbreviation = models.CharField(max_length=3, null=False, blank=True)
    
    def __str__(self):
        return self.name

class Stage(BaseContent):
    form = models.ForeignKey('Form', on_delete = models.CASCADE, null=True, blank=True)
    stage = models.CharField(max_length=255, null=True)
    sequence = models.IntegerField(null=True, blank=True)
    warning_interval = models.DateTimeField(null=True, blank=True)
    urgent_interval = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.stage

class StageAction(BaseContent):
    stage = models.ForeignKey('Stage', on_delete = models.CASCADE, null = True)
    action = models.CharField(max_length=255, null=True, blank=True)
    required = models.BooleanField(default = False)
    optional = models.BooleanField(default = False)
    
    def __str__(self):
        return self.action
   
class Configuration(BaseContent):
    category = models.CharField(max_length=255, null=True, blank=True)
    configuration = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    current_value = models.CharField(max_length=255, null=True, blank=True)
    default_value = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.configuration
    
class Territories(BaseContent):
    use = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Territory"
        verbose_name_plural = "Territories"
    
class Choice(BaseContent):
    selector = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    choice_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    EDIT_CHOICES = (('Custom','Editable'),('System','Non-Editable'))
    editable = models.CharField(max_length=50, null=True, blank=True, choices=EDIT_CHOICES)
    DEFAULT_CHOICES = (('default','Default'),('None',''))
    deafult = models.CharField(max_length=50, null=True, blank=True, choices=DEFAULT_CHOICES)
    
    def __str__(self):
        return self.choice_name
    
class Menu(BaseContent):
    menu_category = models.CharField(max_length = 255, null=True, blank =True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    menu_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.ForeignKey('system.Entity', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.menu_category

class Form(BaseContent):
    form = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.form

class FormList(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True)
    relation = models.CharField(max_length = 255, null=True, blank = True)
    primary = models.BooleanField(default = False)
    position = models.IntegerField(null=True, blank=True)

class FormData(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    data = models.CharField(max_length=255, null=True)
    table = models.CharField(max_length=255, null=True)
    parent_field = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True)
    TYPE_CHOICES = (('dropdown','Dropdown'),('text','Text'),('number','Number'),('checkbox','Checkbox'),
                    ('radio','Radio'), ('link', 'Link'), ('read-only', 'Read-Only'),
                    ('decimal', 'Decimal'), ('button', 'Button'), ('enterable', 'Enterable'),
                    ('composite', 'Composite'))
    type = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_CHOICES)
    link = models.CharField(max_length=255, null = True, blank = True)
    section = models.ForeignKey('FormSection', on_delete=models.SET_NULL, null=True, blank=True)
    column = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.data

class FormSection(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    section_title = models.CharField(max_length=255, null=True)
    section_sequence = models.IntegerField(null=True , blank=True)
    
    def __str__(self):
        return self.section_title

class List(BaseContent):
    list = models.CharField(max_length=255, null=True)
    data_source = models.CharField(max_length=255, null=True)
    sequence = models.IntegerField(null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    def __str__(self):
        return self.list

class ListIcon(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.icon

class Help(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey('Language', on_delete =models.SET_NULL, null =True, blank = True)
    help = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.form
    
class Category(BaseContent):
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tile(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    list_view = models.CharField(max_length = 255, null=True, blank=True)
    search_criteria = models.CharField(max_length = 255, null=True, blank=True)