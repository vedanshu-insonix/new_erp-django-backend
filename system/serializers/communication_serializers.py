from ..models.communication import *
from rest_framework import serializers
from .user_serializers import RelatedUserSerilaizer
from django.db.models.signals import post_save
from django.dispatch import receiver
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers


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
    
    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='channel')
        if record_id:
            data['id']=get_rid_pkey('channel')
        return data


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
            
        #channel = RelatedChannelSerializer(instance.channel).data
        #if 'id' in channel:
        #    response['channel'] = RelatedChannelSerializer(instance.channel).data
        return response
    
    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='communication')
        if record_id:
            data['id']=get_rid_pkey('communication')
        return data

   
class CommunicationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationAddress
        exclude = ("address","id")
        depth = 1

@receiver(post_save, sender=Communication)
def update_comm(created,instance,**kwargs):
    if created==True:
        pass
    else:
        if instance.id is not None:
            addr_rec = CommunicationAddress.objects.filter(communication_id=instance.id)
            if addr_rec:
                comm_rec=Communication.objects.filter(id=instance.id)
                if comm_rec.values()[0]['primary'] == True:
                    if instance.communication_channel=='telephone':
                        address_rec = Addresses.objects.filter(id=addr_rec.values()[0]['address_id']).update(telephone = instance.external_routing,
                                                                                            telephone_type = instance.communication_type)
                    elif instance.communication_channel=='email':
                        address_rec = Addresses.objects.filter(id=addr_rec.values()[0]['address_id']).update(email = instance.external_routing)