from ..models.entity import *
from rest_framework import serializers
from ..serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.common_serializers import RelatedStageSerializer
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers
from sales.models.address import Addresses
from sales.serializers.addresses_serializers import AddressSerializer
from system.serializers.team_serializer import TeamSerializer, Team

#**************************Serializer For Entity Model**************************#
class RelatedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        exclude = ("created_time","modified_time","created_by")

class EntitySerializer(serializers.ModelSerializer):
    billing_address = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_billing_address(self, obj):
        req = self.context['request']
        companyID = obj.id
        queryset = Addresses.objects.filter(company=companyID, address_type__system_name='billing_address')
        serializedData = AddressSerializer(queryset, many=True, context={'request':req})
        return serializedData.data

    def get_shipping_address(self, obj):
        req = self.context['request']
        companyID = obj.id
        queryset = Addresses.objects.filter(company=companyID, address_type__system_name='shipping_address')
        serializedData = AddressSerializer(queryset, many=True, context={'request':req})
        return serializedData.data
        
    def get_user(self, obj):
        req = self.context['request']
        userID = obj.user.all()
        queryset = User.objects.filter(id__in = userID)
        serializer = RelatedUserSerilaizer(queryset, many=True, context={'request':req})
        return serializer.data

    def get_team(self, obj):
        req = self.context['request']
        teamID = obj.team.all()
        queryset = Team.objects.filter(id__in = teamID)
        serializer = TeamSerializer(queryset, many=True, context={'request':req})
        return serializer.data

    class Meta:
        model = Entity
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        req = self.context['request']

        # entity address details
        companyID =instance.id
        address_queryset = Addresses.objects.filter(company=companyID, default=True).first()
        print(address_queryset)
        if address_queryset:
            response['address_id'] = address_queryset.id
        else:
            response['address_id'] = None
        serializer = AddressSerializer(address_queryset, context={'request':req})
        address_values = serializer.data
        for key, value in address_values.items():
            if key == 'id' or key == 'company': pass
            elif key == 'company_name': response[key] = instance.system_name
            else: response[key] = value

        entity_type = instance.entity_type
        if entity_type:
            response['entity_type'] = instance.entity_type.system_name

        stage = instance.stage
        if stage:
            response['stage'] = instance.stage.system_name
        # created_by = RelatedUserSerilaizer(instance.created_by).data
        # if 'id' in created_by:
        #     response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='entity')
        if record_id:
            data['id']=get_rid_pkey('entity')
        return super().create(data)

#**************************Serializer For Entity Address Model**************************#        
# class EntityAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EntityAddress
#         exclude = ("entity","created_time","modified_time","created_by","id")
#         depth = 1

# #**************************Serializer For Entity User Model**************************#
# class EntityUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EntityUser
#         exclude = ("entity","created_time","modified_time","created_by","id")
#         depth = 1

# #**************************Serializer For Entity Team Model**************************#
# class EntityTeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EntityTeam
#         exclude = ("entity","created_time","modified_time","created_by","id")
#         depth = 1