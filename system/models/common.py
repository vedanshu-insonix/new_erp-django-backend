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
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    form = models.ForeignKey('Form', on_delete= models.CASCADE, null = True, blank=True)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    button_type = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.system_name
    
class Currency(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, unique=True, blank=True)
    code = models.CharField(max_length=3, blank=True)
    symbol = models.CharField(max_length=10, blank=True)
    current_rate = models.DecimalField(max_digits= 30, decimal_places=2,null= True, blank=True)
    updated = models.DateTimeField(null=True, unique=True)
    
    def __str__(self):
        return self.system_name

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
     
class Tag(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    tag = models.CharField(max_length=255, null=True, unique=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.tag
    
class Language(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, null=True, unique=True)
    native_name = models.CharField(max_length=255, null=True, unique=True)
    code = models.CharField(max_length=255, null=True, unique=True)
    direction = models.ForeignKey('Choice', on_delete= models.SET_NULL, null=True, related_name="language_direction")
    
    def __str__(self):
        return self.system_name
    
class Country(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    country = CountryField(unique=True, countries_flag_url="/static/flags/{code}.png")
    native_name = models.CharField(max_length=255, null=True, unique= True, blank=True)
    telephone_code = models.CharField(max_length=15, null=True, blank=True)
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
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)
    system_name = models.CharField(max_length=255, null=False, blank=True)
    abbreviation = models.CharField(max_length=10, null=False, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.system_name

class Stage(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    form = models.ForeignKey('Form', on_delete = models.CASCADE, null=True, blank=True)
    system_name = models.CharField(max_length=255, null=True)
    sequence = models.IntegerField(null=True, blank=True)
    warning_interval = models.DateTimeField(null=True, blank=True)
    urgent_interval = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.system_name

class StageAction(BaseContent):
    stage = models.ForeignKey('Stage', on_delete = models.CASCADE, null = True)
    action = models.CharField(max_length=255, null=True, blank=True)
    required = models.BooleanField(default = False)
    optional = models.BooleanField(default = False)
    
    def __str__(self):
        return self.action
   
class Configuration(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    #category = models.CharField(max_length=255, null=True, blank=True)
    system_name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    current_value = models.CharField(max_length=255, null=True, blank=True)
    default_value = models.CharField(max_length=255, null=True, blank=True)
    editable = models.BooleanField(default = False)
    
    def __str__(self):
        return self.system_name
    
class Territories(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    use = models.CharField(max_length=255, null=True, blank=True)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Territory"
        verbose_name_plural = "Territories"

class Selectors(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length = 255, blank=True,unique=True)
    type = models.CharField(max_length = 255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.system_name
        
class Choice(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    selector = models.ForeignKey('Selectors', on_delete=models.CASCADE, null=True, blank=True)
    system_name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    deafult = models.BooleanField(default=False)
    
    def __str__(self):
        return self.system_name
    
class Menu(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length = 255, null=True, blank =True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    menu_category = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    entity = models.ForeignKey('system.Entity', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True , blank=True)
    
    def __str__(self):
        return self.menu_category

class Form(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True , blank=True)
    
    def __str__(self):
        return self.system_name
    
class FormIcon(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey('Icons', on_delete=models.CASCADE, null=True, blank=True)

class FormList(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    relation = models.CharField(max_length = 255, null=True, blank = True)
    primary = models.BooleanField(default = False)
    position = models.IntegerField(null=True, blank=True)

class FormData(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True, blank=True)
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
    visibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.data

class FormSection(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    section_title = models.CharField(max_length=255, null=True)
    section_sequence = models.IntegerField(null=True , blank=True)
    
    def __str__(self):
        return self.section_title

class List(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True , blank=True)
    data_source = models.ForeignKey('DataTable', on_delete=models.CASCADE, null=True, blank=True)
    list_type = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True, related_name='list_type')
    default_view = models.CharField(max_length=255, null=True)
    # visibility = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True, related_name='visibility')
    # data_filter = models.CharField(max_length=255, null=True)
    # data_sort = models.CharField(max_length=255, null=True)
    # sequence = models.IntegerField(null=True , blank=True)

    def __str__(self):
        return self.system_name
    
class ListFilters(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    list = models.ForeignKey('List', on_delete=models.CASCADE)
    data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)
    operator_choice = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    sequence = models.IntegerField(null=True , blank=True)

class ListSorts(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    column = models.ForeignKey('Column', on_delete=models.CASCADE, null=True, blank=True)
    sort_direction = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.IntegerField(null=True , blank=True)

class ListIcon(BaseContent):
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.ForeignKey('Icons', on_delete=models.CASCADE, null=True, blank=True)

class Help(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey('Language', on_delete =models.SET_NULL, null =True, blank = True)
    help = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.form
    
class Category(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tile(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)
    list_view = models.CharField(max_length = 255, null=True, blank=True)
    search_criteria = models.CharField(max_length = 255, null=True, blank=True)

class Icons(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon_image = models.FileField(upload_to='icon_images/', max_length=255, null=True, blank=True)