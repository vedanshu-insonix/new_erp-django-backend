from ..models.communication import *
from rest_framework import serializers
from .user_serializers import RelatedUserSerilaizer
from django.db.models.signals import post_save
from django.dispatch import receiver


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

@receiver(post_save, sender=Communication)
def alert_msg(created,instance,**kwargs):
    if created==True:
        pass
    else:
        if instance.id is not None:
            comm_rec = CommunicationAddress.objects.get(communication_id=instance.id)
            #serializer = CommunicationSerializer(data=instance, partial=True)
            #if serializer.is_valid():
            #    serializer.save()
            if instance.primary:
                if instance.primary == True:
                    if instance.communication_channel=='telephone':
                        address_rec = Address.objects.filter(id=comm_rec.address_id).update(telephone = instance.external_routing,
                                                                                            telephone_type = instance.communication_type,
                                                                                            type = 'communication')
                    elif instance.communication_channel=='email':
                        address_rec = Address.objects.filter(id=comm_rec.address_id).update(email = instance.external_routing,
                                                                                            type = 'communication')
                    #elif instance.communication_channel=='3' or instance.communication_channel=='4':
                    #    address_rec = Address.objects.filter(id=comm_rec.address_id).update(other_communication = instance.external_routing,
                    #                                                                        other_communication_type = instance.communication_channel,
                    #                                                                        type = 'communication')