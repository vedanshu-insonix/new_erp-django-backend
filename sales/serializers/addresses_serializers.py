from rest_framework import serializers
from ..models.address import Addresses
from system.serializers.common_serializers import *
# from system.serializers.user_serializers import RelatedUserSerilaizer
from system.models.communication import Communication
from system.serializers.communication_serializers import RelatedCommunicationSerializer
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers


#**************************Serializer For Addresses Model**************************#
class RelatedAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ("__all__")
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail 
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']

        state = RelatedStateSerializer(instance.state, context={'request': request}).data
        if 'id' in state:
            response['state'] = RelatedStateSerializer(instance.state, context={'request': request}).data
            
        country = RelatedCountrySerializer(instance.country, context={'request': request}).data
        if 'id' in country:
            response['country'] = RelatedCountrySerializer(instance.country, context={'request': request}).data
            
        language = RelatedLanguageSerializer(instance.language, context={'request': request}).data
        if 'id' in language:
            response['language'] = RelatedLanguageSerializer(instance.language, context={'request': request}).data

        stage = RelatedStageSerializer(instance.stage, context={'request': request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request': request}).data
        
        customerRec = instance.customer
        if customerRec:
            response['customer'] = customerRec.customer

        vendorRec = instance.vendor
        if vendorRec:
            response['vendor'] = vendorRec.vendor

        entityRec = instance.company
        if entityRec:
            response['company'] = entityRec.system_name
        
        typeRec = instance.address_type
        if typeRec:
            response['address_type'] = typeRec.system_name
        
        locTypeRec = instance.address_location_type
        if locTypeRec:
            response['address_location_type'] = locTypeRec.system_name

        telephoneType = instance.telephone_type
        if telephoneType:
            response['telephone_type'] = telephoneType.system_name

        otherType = instance.other_communication_type
        if otherType:
            response['other_communication_type'] = otherType.system_name

        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='addresses')
        if record_id:
            data['id']=get_rid_pkey('addresses')
        return super().create(data)