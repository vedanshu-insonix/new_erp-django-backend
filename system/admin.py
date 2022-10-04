from dataclasses import field
from django.contrib import admin
from .models.common import *
from .models.columns import *
from .models.translations import *

# Register your models here.

admin.site.register([State, Country, Menu, Form, Tag, App, Field, Language, List, Translation])

