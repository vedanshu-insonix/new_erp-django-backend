from django.db import models
from system.models.common import BaseContent

class Receipts(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    date = models.DateTimeField(null = True, blank = True)
    amount = models.DecimalField(max_digits=30,decimal_places=2,null=True, blank=True)
    currency = models.ForeignKey('system.Currency', on_delete = models.SET_NULL, null= True, blank = True)
    receipt_for = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null = True, blank = True)
    sales_invoice = models.ForeignKey('SalesInvoices', on_delete = models.SET_NULL, null= True, blank = True)
    #vendor_refund = models.ForeignKey('VendorRefunds', on_delete = models.SET_NULL, null= True, blank = True)
    stage = models.ForeignKey('system.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="receipt_status")