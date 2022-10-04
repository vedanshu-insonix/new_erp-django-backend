from django.db import models
from .common import BaseContent
from sales.models.address import Address
from ..utils import ChannelTypeChoice

class Communication(BaseContent):
    primary = models.BooleanField(default=False)
    channel = models.ForeignKey('Channel', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=255, choices=ChannelTypeChoice, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    routing = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.channel
    

class Channel(BaseContent):
    name = models.CharField(max_length=255,null=True, blank=True)
    
    def __str__(self):
        return self.name

class CommunicationAddress(BaseContent):
    communication = models.ForeignKey('Communication', on_delete=models.CASCADE, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, unique=True)
