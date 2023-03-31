from ..models.entity import *
from rest_framework import serializers
from system.models.roles_permissions import *
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey

#**************************Serializer For Permission Model**************************#
class PermissionSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        queryset = RolePermissions.objects.filter(permissions=obj.id)
        serializer = RolePermissionSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['role']) if serializer.data else None
        return result

    class Meta:
        model = Permission
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='permission')
        if record_id:
            data['id']=get_rid_pkey('permission')
        return super().create(data)

#**************************Serializer For Role Model**************************#    
class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        queryset = RolePermissions.objects.filter(role=obj.id)
        serializer = RolePermissionSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['permissions']) if serializer.data else None
        return result

    class Meta:
        model = Role
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='role')
        if record_id:
            data['id']=get_rid_pkey('role')
        return super().create(data)

#**************************Serializer For Role Permissions Model**************************#
class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermissions
        fields = ("__all__")
        depth = 1

#**************************Serializer For Role Categories Model**************************#
class RoleCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleCategories
        fields = ("__all__")

#**************************Serializer For Role Territories Model**************************#
class RoleTerritoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleTerritories
        fields = ("__all__")