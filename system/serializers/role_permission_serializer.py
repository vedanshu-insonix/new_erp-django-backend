from ..models.company import *
from rest_framework import serializers
from system.models.roles_permissions import *

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("__all__")

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("__all__")

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermissions
        fields = ("__all__")

class RoleCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategories
        fields = ("__all__")

class RoleTerritoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleTerritories
        fields = ("__all__")