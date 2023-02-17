from email.policy import default
from enum import unique
from django.db import models
from system.utils import DateFormatChoices, TimeFormatChoice, ColumnVisibilityChoice
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
    name = models.CharField(max_length=255, unique=True, blank=True)
    code = models.CharField(max_length=3, blank=True)
    symbol = models.CharField(max_length=10, blank=True)
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
    native_Translation = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, blank=True)
    #direction=models.CharField(max_length=255, null=True, blank=True)
    direction =models.ForeignKey('Choice', on_delete= models.CASCADE, null = True, blank=True)
    # date_format = models.CharField(max_length=255, choices=DateFormatChoices, null=True, blank=True)
    # time_format = models.CharField(max_length=255, choices=TimeFormatChoice, null=True, blank=True)
    # symbol_position = models.IntegerField(null=True, blank=True)
    # thousands_separator = models.CharField(max_length=255, null=True, blank=True)
    # fraction_separator = models.CharField(max_length=255, null=True, blank=True)
    # decimal_places = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Country(BaseContent):
    country = CountryField(max_length=255,unique=True, countries_flag_url="/static/flags/{code}.png")
    native_name = models.CharField(max_length=255, null=True, unique= True, blank=True)
    telephone_code = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey('Currency', on_delete= models.SET_NULL, null=True, blank=True)
    symbol_position = models.ForeignKey('Choice', on_delete= models.SET_NULL, null=True, related_name="country_symbol_position")
    money_format = models.ForeignKey('Choice', on_delete= models.SET_NULL, null=True, related_name="country_money_format")
    date_format = models.ForeignKey('Choice', on_delete= models.SET_NULL, null=True, related_name="country_date_format")
    time_format = models.ForeignKey('Choice', on_delete= models.SET_NULL, null=True, related_name="country_time_format")
    
    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class State(BaseContent):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=False, blank=True)
    abbreviation = models.CharField(max_length=255, null=False, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    
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
    #category = models.CharField(max_length=255, null=True, blank=True)
    configuration = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    current_value = models.CharField(max_length=255, null=True, blank=True)
    default_value = models.CharField(max_length=255, null=True, blank=True)
    editable = models.BooleanField(default= False)
    
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

class Selectors(BaseContent):
    selector = models.CharField(max_length = 255, blank=True,unique=True)
    type = models.CharField(max_length = 255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.selector
        
class Choice(BaseContent):
    selector = models.ForeignKey('Selectors', on_delete=models.CASCADE, null=True, blank=True)
    choice_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    # EDIT_CHOICES = (('Custom','Editable'),('System','Non-Editable'))
    # editable = models.CharField(max_length=50, null=True, blank=True, choices=EDIT_CHOICES)
    deafult = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_name
    
class Menu(BaseContent):
    name = models.CharField(max_length=255,null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category_choice = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.menu_category

class Form(BaseContent):
    form = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True , blank=True)
    form_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.form
    
class FormIcon(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey('Icons', on_delete=models.CASCADE, null=True, blank=True)

class FormList(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
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
    system_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True , blank=True)
    primary_table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True, blank=True)
    list_type = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True, related_name='list_type')
    default_view = models.CharField(max_length=255, null=True)
    visibility = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True, related_name='list_visibility')

   
class ListFilters(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE)
    data = models.ForeignKey('Data', on_delete=models.CASCADE)
    operator_choice = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    sequence = models.IntegerField(null=True , blank=True)

class ListSorts(BaseContent):
    column = models.ForeignKey('Column', on_delete=models.CASCADE, null=True, blank=True)
    sort_direction = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True , blank=True)

class ListIcon(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey('Icons', on_delete=models.CASCADE, null=True, blank=True)

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

class Icons(BaseContent):
    system_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon_image = models.FileField(upload_to='icon_images/', max_length=255, null=True, blank=True)
    usage = models.CharField(max_length=255, null=True, blank=True)