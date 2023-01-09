from rest_framework import viewsets
from system.models.roles_permissions import *
from system.serializers.role_permission_serializer import *

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Team to be modified.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class RoleViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamRole to be modified.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamUser to be modified.
    """
    queryset = RolePermissions.objects.all()
    serializer_class = RolePermissionSerializer

class RoleCategoriesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamUser to be modified.
    """
    queryset = RoleCategories.objects.all()
    serializer_class = RoleCategoriesSerializer

class RoleTerritoriesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamUser to be modified.
    """
    queryset = RoleTerritories.objects.all()
    serializer_class = RoleTerritoriesSerializer