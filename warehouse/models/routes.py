from django.db import models
from system.models.common import *

class Routes(BaseContent):
    ApplicationChoice =(("Sales Orders","sales orders"),("Sales Return Orders","sales return orders"),("Purchase Orders","purchase orders"),
                        ("Purchase Return Orders","purchase return orders"),("Manufacturing Orders","manufacturing orders"),("Transfer Orders","transfer orders"))
    route_application=models.CharField(max_length = 255, null=True, blank=True, choices=ApplicationChoice)
    route_type=models.CharField(max_length=255, null=True, blank=True)
    code=models.CharField(max_length=255, null=True, blank=True)
    identifier=models.CharField(max_length=255, null=True, blank=True)
    description=models.CharField(max_length=255, null=True, blank=True)
    stage=models.ForeignKey('system.Stage', on_delete = models.SET_NULL, null=True, blank=True)
    status=models.CharField(max_length = 255, null=True, blank=True)

class Route_Types(BaseContent):
    route_usage=models.CharField(max_length = 255, null=True, blank=True)
    name=models.CharField(max_length = 255, null=True, blank=True)
    code=models.CharField(max_length = 255, null=True, blank=True)

class Route_Type_Rules(BaseContent):
    route_type=models.ForeignKey(Route_Types, on_delete = models.SET_NULL, null=True, blank=True)
    rule=models.ForeignKey('system.Rules', on_delete = models.SET_NULL, null=True, blank=True)