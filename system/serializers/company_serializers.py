from ..models.company import *
from rest_framework import serializers
from ..serializers.user_serializers import RelatedUserSerilaizer


class RelatedCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ("created_time","modified_time","created_by")

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
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