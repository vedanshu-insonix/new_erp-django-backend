from django.contrib import admin
from .models.manufacturing import Manufacturingorderlines, Manufacturingorders
from .models.purchase import PurchaseOrder, PurchaseOrderLines, Disbursment

# Register your models here. 
admin.site.register([Manufacturingorderlines, Manufacturingorders,PurchaseOrder, PurchaseOrderLines, Disbursment])
