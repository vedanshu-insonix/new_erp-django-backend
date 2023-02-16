from django.db import models
from system.models.common import BaseContent

class SalesPriceLists(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length = 255, null = True, blank = True)
    customer = models.ForeignKey('Customers', on_delete = models.CASCADE, null = True, blank = True)
    category_id = models.ForeignKey('system.Category', on_delete = models.CASCADE, null = True, blank = True) 