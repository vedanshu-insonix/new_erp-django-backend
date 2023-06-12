from django.contrib import admin
from .models.general import *
from .models.operation import *
from .models.products import *
from .models.routes import *
from .models.shipping_models import *

# Register your models here.
admin.site.register([Journal, JournalTemplate, Attributes, Images, Operations, Transfers, Product, Bom, Components, Characteristics, Locations, ProductCategory,
                     ProductCounts, Equivalents, ProductLocations, UOM, ProductLine, Routes, RouteTypes, RouteTypeRules, Deliveries,DeliveryLines, Shipments,
                     Containers, ContainerTypes, Contents])
