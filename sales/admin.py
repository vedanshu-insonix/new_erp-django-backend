#from tkinter import S
from django.contrib import admin
from .models.vendors import Vendors
from .models.customers import Customers, CustomerAddress
from .models.address import Addresses, AddressTag
from .models.quotations import SalesQuotations
# Register your models here. 
admin.site.register([Customers, Addresses,Vendors, CustomerAddress, AddressTag, SalesQuotations])