from rest_framework import serializers
from system.models.recordid import RecordIdentifiers

class RecordIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordIdentifiers
        fields = ("__all__")