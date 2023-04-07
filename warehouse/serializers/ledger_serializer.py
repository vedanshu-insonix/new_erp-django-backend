from rest_framework import serializers
from system.serializers.user_serializers import RelatedUserSerilaizer
from warehouse.models.ledger import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Accounts Model**************************#
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='accounts')
        if record_id:
            data['id']=get_rid_pkey('accounts')
        return super().create(data)
    