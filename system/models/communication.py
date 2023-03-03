from django.db import models
from .common import BaseContent
from sales.models.address import Addresses
from ..utils import ChannelTypeChoice

class Communication(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    primary = models.BooleanField(default=False)
    communication_channel = models.CharField(max_length=255, null=True, blank=True)
    communication_type = models.CharField(max_length=255, choices=ChannelTypeChoice, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    routing = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.communication_channel
    

class Channel(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    name = models.CharField(max_length=255,null=True, blank=True)
    
    def __str__(self):
        return self.name

class CommunicationAddress(BaseContent):
    communication = models.OneToOneField('Communication', on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE, null=True)