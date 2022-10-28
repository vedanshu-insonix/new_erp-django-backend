from email.policy import default
from enum import unique
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
    symbol_position = models.IntegerField(null=True, blank=True)
    thousands_separator = models.CharField(max_length=255, null=True, blank=True)
    fraction_separator = models.CharField(max_length=255, null=True, blank=True)
    decimal_places = models.IntegerField(null=True, blank=True)
    
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
        verbose_name = "Territories"
        verbose_name_plural = "Territories"
    
class Choice(BaseContent):
    form = models.ForeignKey('Form', on_delete = models.CASCADE, null=True, blank=True)
    selector = models.CharField(max_length = 255, null=True, blank = True)
    choice = models.CharField(max_length=255, null=True)
    sequence = models.IntegerField(null=True, blank=True)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice
    
# class Field(BaseContent):
#     application = models.ForeignKey('App', on_delete=models.CASCADE, null=True, blank=True)
#     form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
#     field = models.CharField(max_length=255, null=True, blank=True)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     TYPE_CHOICES = (('dropdown','Dropdown'),('text','Text'),('number','Number'),('checkbox','Checkbox'),('radio','Radio'))
#     type = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_CHOICES)
#     data_source = models.CharField(max_length=50, null=True, blank=True)
#     panel = models.IntegerField(null=True, blank=True)
#     position = models.IntegerField(null=True, blank=True)
    
#     def __str__(self):
#         return self.name

class Menu(BaseContent):
    menu_category = models.CharField(max_length = 255, null=True, blank =True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.menu_category

class Form(BaseContent):
    # menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, null=True, blank=True)
    form = models.CharField(max_length=255, null=True, unique=True)
    
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
    TYPE_CHOICES = (('dropdown','Dropdown'),('text','Text'),('number','Number'),('checkbox','Checkbox'),('radio','Radio'))
    type = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_CHOICES)
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
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    list = models.CharField(max_length=255, null=True)
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

# class FieldConfiguration(BaseContent):
#     form_data = models.ForeignKey('FormData', on_delete=models.CASCADE, null = True)
#     type  = models.CharField(max_length=255, null=True, blank = True)
#     default_value = models.CharField(max_length=255, null=True, blank = True)
#     editable = models.BooleanField(null=True, blank = True)
    
# class ThemeConfiguration(BaseContent):
#     configuration = models.CharField(max_length=255, null=True, blank = True)
#     type  = models.CharField(max_length=255, null=True, blank = True)
#     default_value = models.CharField(max_length=255, null=True, blank = True)
#     editable = models.BooleanField(null=True, blank = True)

# class Configuration(BaseContent):
    
    