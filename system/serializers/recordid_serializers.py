from rest_framework import serializers
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Record Identifier Model**************************#
class RecordIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordIdentifiers
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}