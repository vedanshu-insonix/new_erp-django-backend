#from tkinter import S
from django.contrib import admin
from .models.vendors import Vendors, VendorProducts, VendorPrices
from .models.customers import *
from .models.address import *
from .models.quotations import *
from .models.carts import *
from .models.invoices import *
from .models.pricelist import *
from .models.receipts import *
from .models.returns import *
from .models.sales_credit import *
from .models.sales_orders import *
# Register your models here. 
admin.site.register([Customers, Addresses, Vendors, SalesQuotations, Cartlines, Carts,
                     SalesCredits, SalesInvoices, SalesOrderLines, SalesOrders, SalesPriceLists, Receipts, SalesReturns,
                     SalesReturnLines, VendorProducts, VendorPrices])