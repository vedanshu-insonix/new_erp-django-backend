from django.db import models
from .common import BaseStatus, BaseContent
# from sales.models.address import Addresses

class Communication(BaseStatus):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    primary = models.BooleanField(default=False)
    communication_channel = models.CharField(max_length=255, null=True, blank=True)
    communication_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_communication_type")
    value = models.CharField(max_length=255, null=True, blank=True)
    routing = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)
    address = models.ForeignKey('sales.Addresses', on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_address")

    def __str__(self):
        return self.communication_channel
    

class Channel(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    name = models.CharField(max_length=255,null=True, blank=True)
    
    def __str__(self):
        return self.name

# class CommunicationAddress(BaseContent):
#     communication = models.OneToOneField('Communication', on_delete=models.CASCADE, null=True)
#     address = models.ForeignKey(Addresses, on_delete=models.CASCADE, null=True)