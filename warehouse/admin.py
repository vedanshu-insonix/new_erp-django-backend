from django.contrib import admin
from .models.general import *
from .models.operation import *
from .models.products import *
from .models.routes import *
from .models.shipping_models import *

# Register your models here.
admin.site.register([Journal, JournalTemplate, Attributes, ProductAttribute, Images, ProductImages,
                     Operations, Transfers, Product, Bom, Components, Characteristics, Value, Locations, ProductCategory,
                     ProductCounts, Equivalents, ProductValues, ProductLocations, UOM, ProductLine, Routes, RouteTypes, RouteTypeRules, Deliveries,
                     DeliveryLines, Shipments, Containers, ContainerTypes, Contents])
