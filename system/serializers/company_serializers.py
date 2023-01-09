from ..models.company import *
from rest_framework import serializers
from ..serializers.user_serializers import RelatedUserSerilaizer
from system.serializers.common_serializers import RelatedStageSerializer


class RelatedCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ("created_time","modified_time","created_by")

class CompanySerializer(serializers.ModelSerializer):
    billing_address = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_billing_address(self, obj):
        queryset = CompanyAddress.objects.filter(company=obj.id)
        serializer = CompanyAddressSerializer(queryset, many=True)
        return serializer.data

    def get_shipping_address(self, obj):
        queryset = CompanyAddress.objects.filter(company=obj.id)
        serializer = CompanyAddressSerializer(queryset, many=True)
        return serializer.data

    def get_users(self, obj):
        queryset = CompanyUser.objects.filter(company = obj.id)
        serializer = CompanyUserSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Company
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']

        stage = RelatedStageSerializer(instance.stage, context={'request': request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
        
class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        exclude = ("address","id")
        depth = 1

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ("__all__")