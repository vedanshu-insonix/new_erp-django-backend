from django.db import models
from system.models.common import *

class Rules(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length = 255, null=True, blank=True)
    rule_action = models.CharField(max_length = 255, null=True, blank=True)##Fkey Lookup
    rule_origin = models.CharField(max_length = 255, null=True, blank=True)##Fkey Lookup
    rule_destination = models.CharField(max_length = 255, null=True, blank=True)##Fkey Lookup
    rule_trigger = models.CharField(max_length = 255, null=True, blank=True)##Fkey Lookup
    description = models.CharField(max_length = 255, null=True, blank=True)