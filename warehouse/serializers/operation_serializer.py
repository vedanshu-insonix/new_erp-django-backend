from rest_framework import serializers
from warehouse.models.operation import *

class Operation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = ('__all__')