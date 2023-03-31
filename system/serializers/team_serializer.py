from ..models.entity import *
from rest_framework import serializers
from system.models.teams import *
from system.serializers.role_permission_serializer import RoleSerializer
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey

#**************************Serializer For Team Model**************************#
class TeamSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_users(self, obj):
        queryset = TeamUser.objects.filter(team=obj.id)
        serializer = TeamUserSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['user']) if serializer.data else None
        return result

    def get_roles(self, obj):
        queryset = TeamRole.objects.filter(team=obj.id)
        serializer = TeamRoleSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['role']) if serializer.data else None
        return result

    class Meta:
        model = Team
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='team')
        if record_id:
            data['id']=get_rid_pkey('team')
        return super().create(data)

#**************************Serializer For Team Role Model**************************#
class TeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRole
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        role = RoleSerializer(instance.role, context={'request':request}).data
        if 'id' in role:
            response['role'] = RoleSerializer(instance.role, context={'request':request}).data
        return response  

#**************************Serializer For Team User Model**************************#
class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        exclude = ("created_time","modified_time","created_by", "team")
        depth = 1