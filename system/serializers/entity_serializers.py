from ..models.entity import *
from rest_framework import serializers
from ..serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.common_serializers import RelatedStageSerializer
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Entity Model**************************#
class RelatedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        exclude = ("created_time","modified_time","created_by")

class EntitySerializer(serializers.ModelSerializer):
    billing_address = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    def get_billing_address(self, obj):
        queryset = EntityAddress.objects.filter(entity=obj.id, address__address_type='billing_address')
        serializer = EntityAddressSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['address']) if serializer.data else None
        return result

    def get_shipping_address(self, obj):
        queryset = EntityAddress.objects.filter(entity=obj.id, address__address_type='shipping_address')
        serializer = EntityAddressSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['address']) if serializer.data else None
        return result
        
    def get_users(self, obj):
        queryset = EntityUser.objects.filter(entity = obj.id)
        serializer = EntityUserSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['user']) if serializer.data else None
        return result

    def get_teams(self, obj):
        queryset = EntityTeam.objects.filter(entity = obj.id)
        serializer = EntityTeamSerializer(queryset, many=True)
        result=[]
        for i in range(len(serializer.data)):
            result.append(serializer.data[i]['team']) if serializer.data else None
        return result

    class Meta:
        model = Entity
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']

        entity_type = instance.entity_type
        if entity_type:
            response['entity_type'] = instance.entity_type.system_name
        stage = RelatedStageSerializer(instance.stage, context={'request': request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='entity')
        if record_id:
            data['id']=get_rid_pkey('entity')
        return super().create(data)

#**************************Serializer For Entity Address Model**************************#        
class EntityAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityAddress
        exclude = ("entity","created_time","modified_time","created_by","id")
        depth = 1

#**************************Serializer For Entity User Model**************************#
class EntityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityUser
        exclude = ("entity","created_time","modified_time","created_by","id")
        depth = 1

#**************************Serializer For Entity Team Model**************************#
class EntityTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityTeam
        exclude = ("entity","created_time","modified_time","created_by","id")
        depth = 1