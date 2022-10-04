from ..models.communication import *
from rest_framework import serializers
from .user_serializers import RelatedUserSerilaizer


class RelatedChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ("__all__")

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
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


class RelatedCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        exclude = ("created_time", "modified_time", "created_by")
        

class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        channel = RelatedChannelSerializer(instance.channel).data
        if 'id' in channel:
            response['channel'] = RelatedChannelSerializer(instance.channel).data
        return response

   
class CommunicationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationAddress
        exclude = ("address","id")
        depth = 1