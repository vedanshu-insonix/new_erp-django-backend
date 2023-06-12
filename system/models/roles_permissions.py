from django.db import models
from system.models.common import BaseContent
from django.contrib.auth.models import User

class Permission(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length = 255, null= True, blank=True, unique=True)
    description = models.TextField(null= True, blank=True)
    # visibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    # entity = models.ForeignKey('Entity', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.system_name
    
class Role(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    editable = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    permissions = models.ManyToManyField('Permission', blank=True, related_name='role')
    user = models.ManyToManyField(User, blank=True, related_name='role')
    category = models.ForeignKey('Category', on_delete = models.CASCADE, null=True, blank=True, related_name='role')
    territories = models.ForeignKey('Territories', on_delete = models.CASCADE, null=True, blank=True, related_name='role')

    
    def __str__(self):
        return self.system_name

# class RolePermissions(BaseContent):
#     role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
#     permissions = models.ForeignKey('Permission', on_delete = models.CASCADE, null=True, blank=True)

# class RoleCategories(BaseContent):
#     role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
#     category = models.ForeignKey('Category', on_delete = models.CASCADE, null=True, blank=True, related_name='role')
    
    
# class RoleTerritories(BaseContent):
#     role = models.ForeignKey('Role', on_delete = models.CASCADE, null=True, blank=True)
#     territories = models.ForeignKey('Territories', on_delete = models.CASCADE, null=True, blank=True, related_name='role')
    