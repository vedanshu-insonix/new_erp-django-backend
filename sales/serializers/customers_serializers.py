from rest_framework import serializers
from ..models.customers import Customer, CustomerAddress
from system.serializers.common_serializers import *
from system.serializers.user_serializers import RelatedUserSerilaizer

class RelatedCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ("created_time","modified_time","created_by")

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        sales_currency_data = RelatedCurrencySerializer(instance.sales_currency).data
        if 'id' in sales_currency_data:
            response['sales_currency'] = RelatedCurrencySerializer(instance.sales_currency).data
            
        stage_data = RelatedStageSerializer(instance.stage).data
        if 'id' in stage_data:
            response['stage'] = RelatedStageSerializer(instance.stage).data
            
        created_data = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_data:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        parent_data = RelatedCustomerSerializer(instance.parent_id).data
        if 'id' in parent_data:
            response['parent_id'] = RelatedCustomerSerializer(instance.parent_id).data
        return response

    # def create(self, validated_data):
    #     # profile_data = validated_data.pop('profile')
    #     # user = User.objects.create(**validated_data)
    #     # Profile.objects.create(user=user, **profile_data)
    #     print(validated_data)
    #     return validated_data
  
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        exclude = ("address","id","created_time","modified_time","created_by")
        depth = 1