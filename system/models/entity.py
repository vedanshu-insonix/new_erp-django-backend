from django.db import models
from system.models.common import BaseContent
from django.contrib.auth.models import User
from sales.models.address import Addresses

class Entity(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    EntityTypeChoice =(("1","Entity1"),("2","Entity2"),
                    ("3","Entity3"),("4","Entity4")
                    )
    entity_type = models.CharField(max_length=255, null=True, blank=True, choices=EntityTypeChoice)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    stage_started = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
    

class EntityUser(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.user
    
class EntityAddress(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True)
    #address = models.OneToOneField(Addresses, on_delete=models.CASCADE, null=True, unique=True)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.address
    
class EntityProducts(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE, null=True, blank=True)

class EntityTeam(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)

class EntityAccounts(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    #accounts = models.ForeignKey('warehouse.Accounts', on_delete=models.CASCADE, null=True, blank=True)

class EntityForms(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)

class EntityList(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)

class EntityMenuItem(BaseContent):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, blank=True)