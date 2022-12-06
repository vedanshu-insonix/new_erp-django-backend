from django.db import models
from system.models.common import BaseContent
from system.models.common import *
from system.utils import LocationChoice, StatusChoice

class Journal(BaseContent):
    journal_type = models.CharField(max_length = 255, null=True, blank=True)# FKEY Lookup Field
    journal = models.CharField(max_length = 255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Journal_Template(BaseContent):
    journal = models.ForeignKey('Journal', on_delete=models.SET_NULL, null=True, blank=True)
    journal_template_name = models.CharField(max_length = 255, null=True, blank=True)
    recurring_start_date = models.DateTimeField(null=True, blank=True)

class Attributes(BaseContent):
    attribute = models.CharField(max_length = 255, null=True, blank=True)

    def __str__(self):
        return str(self.attribute)
        
class Product_Attribute(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    attribute = models.ForeignKey('Attributes', on_delete=models.SET_NULL, null=True, blank=True)

class Images(BaseContent):
    image = models.FileField(upload_to='products', max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.CharField(max_length=255, null=True, blank=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice, null=True, blank=True)

    def __str__(self):
        return str(self.image)
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

class Product_Images(BaseContent):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True, blank=True)