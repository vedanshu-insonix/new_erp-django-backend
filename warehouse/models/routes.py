from django.db import models
from system.models.common import *

class Routes(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    route_application=models.ForeignKey('system.Choice', on_delete=models.SET_NULL, null=True, blank=True)
    route_type=models.ForeignKey('RouteTypes', on_delete=models.SET_NULL, null=True, blank=True)
    #code=models.CharField(max_length=255, null=True, blank=True)
    identifier=models.CharField(max_length=255, null=True, blank=True)
    description=models.CharField(max_length=255, null=True, blank=True)
    stage=models.ForeignKey('system.Stage', on_delete = models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length = 255, null=True, blank=True)

class RouteTypes(BaseContent):
    id = models.CharField(max_length=255,primary_key=True)
    route_usage=models.CharField(max_length = 255, null=True, blank=True)
    name=models.CharField(max_length = 255, null=True, blank=True)
    code=models.CharField(max_length = 255, null=True, blank=True)

class RouteTypeRules(BaseContent):
    route_type=models.ForeignKey('RouteTypes', on_delete = models.SET_NULL, null=True, blank=True)
    rule=models.ForeignKey('system.Rules', on_delete = models.SET_NULL, null=True, blank=True)