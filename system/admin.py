from dataclasses import field
from django.contrib import admin
from .models.common import *
from .models.columns import *
from .models.translations import *
from .models.users import *
from .models.communication import *
from .models.dataset import *
from .models.entity import *
from .models.recordid import RecordIdentifiers
from .models.roles_permissions import *
from .models.rules import *
from .models.teams import *

# Register your models here.
admin.site.register([State, Country, Menu, Form, Tag, Language, List, Translation,
                     Choice, FormData, FormList, Column, FormSection, StageAction,
                     Configuration, Communication,Button, Currency, Stage, Team,
                     Territories, Selectors, ListFilters, ListSorts, Help, Category,
                     Tile, Icons, Channel, DataTable, Data, Entity, RecordIdentifiers,
                     Permission, Role, Rules])

