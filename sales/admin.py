from tkinter import S
from django.contrib import admin
from .models.vendors import Vendor
from .models.customers import Customer, CustomerAddress, Currency, Stage
from .models.address import Address, AddressTag
# Register your models here. 
admin.site.register([Customer, Currency, Stage, Address,Vendor, CustomerAddress, AddressTag])