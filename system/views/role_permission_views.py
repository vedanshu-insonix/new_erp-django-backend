from rest_framework import viewsets
from system.models.roles_permissions import *
from system.serializers.role_permission_serializer import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from system import utils

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Team to be modified.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class RoleViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamRole to be modified.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request):
        try:
            data = request.data
            havePermission = False
            if 'permissions' in data:
                permissions = data.pop('permissions')
                havePermission = True
            serializer = RoleSerializer(data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                role_id = serializer.data.get('id')
                new_role = Role.objects.get(id=role_id)
                if havePermission == True:
                    for permission in permissions:
                        permission_name = permission.get('permission')
                        check = Permission.objects.filter(permission=permission_name)
                        if check:
                            permission_id = Permission.objects.get(permission=permission_name)
                            create_role_permission=RolePermissions.objects.create(role=new_role, permissions=permission_id)
                        else:
                            new_permission = PermissionSerializer(data=permission, context={'request':request})
                            if new_permission.is_valid(raise_exception=True):
                                new_permission.save()
                                permission_id=new_permission.data.get('id')
                                permission_id=Permission.objects.get(id=permission_id)
                                create_role_permission=RolePermissions.objects.create(role=new_role, permissions=permission_id)
                new_role = Role.objects.get(id=role_id)
                result = RoleSerializer(new_role, context={'request':request})
            return Response(utils.success_msg(self,result.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))

    def update(self, request, pk):
        try:
            data = request.data
            role_rec = Role.objects.get(id=pk)
            addPermission = False
            removePermission = False
            if 'add_permissions' in data:
                add_permissions = data.pop('add_permissions')
                addPermission = True
            if 'remove_permissions' in data:
                remove_permissions = data.pop('remove_permissions')
                removePermission = True
            serializer = RoleSerializer(role_rec, data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if addPermission == True:
                    for permission in add_permissions:
                        permission_name = permission.get('permission')
                        find = Permission.objects.filter(permission=permission_name)
                        if find:
                            permission_id = Permission.objects.get(permission=permission_name)
                            check = RolePermissions.objects.filter(role=role_rec, permissions=permission_id)
                            if check:
                                pass
                            else:
                                create_role_permission=RolePermissions.objects.create(role=role_rec, permissions=permission_id)
                        else:
                            new_permission = PermissionSerializer(data=permission, context={'request':request})
                            if new_permission.is_valid(raise_exception=True):
                                new_permission.save()
                                permission_id=new_permission.data.get('id')
                                permission_id=Permission.objects.get(id=permission_id)
                                create_role_permission=RolePermissions.objects.create(role=role_rec, permissions=permission_id)
                if removePermission == True:
                    for permission in remove_permissions:
                        permission_name = permission.get('permission')
                        find = Permission.objects.filter(permission=permission_name)
                        if find:
                            permission_id = Permission.objects.get(permission=permission_name)
                            check = RolePermissions.objects.filter(role=role_rec, permissions=permission_id)
                            if check:
                                RolePermissions.objects.get(role=role_rec, permissions=permission_id).delete()
                            else:
                                pass
                msg = "Role Updation Successful."
            return Response(utils.success_msg(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

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