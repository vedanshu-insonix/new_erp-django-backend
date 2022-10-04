from unittest.util import _MAX_LENGTH
from django.db import models
from system.models.common import BaseContent
from django.contrib.auth.models import User

class Permission(BaseContent):
    permission = models.CharField(max_length = 255, null= True, blank=True)
    description = models.TextField(null= True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Role(BaseContent):
    name = models.CharField(max_length=255, null=True, blank=True)
    editable = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class RolePermissions(BaseContent):
    role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
    permissions = models.ForeignKey('Permission', on_delete = models.CASCADE, null=True, blank=True)

class RoleCategories(BaseContent):
    role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete = models.CASCADE, null=True, blank=True)
    
class RoleTerritories(BaseContent):
    role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
    Territories = models.ForeignKey('Territories', on_delete = models.CASCADE, null=True, blank=True)