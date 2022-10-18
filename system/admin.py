from dataclasses import field
from django.contrib import admin
from .models.common import *
from .models.columns import *
from .models.translations import *
from .models.users import *

# Register your models here.
admin.site.register([State, Country, Menu, Form, Tag, App, Field, Language, List, Translation,
                     TranslationFromData, Choice, FormData, FormList, Column, TranslationChoice,
                     UserAddress, TranslationColumn, TranslationForm, FormSection, StageAction])

