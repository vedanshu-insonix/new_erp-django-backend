from rest_framework import serializers
from warehouse.models.routes import *
from warehouse.models.operation import Operations
from warehouse.serializers.operation_serializer import Operation_Serializer

class Route_Serializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField()

    def get_steps(self, obj):
        queryset = Operations.objects.filter(route = obj.id)
        serializer = Operation_Serializer(queryset, many=True)
        return serializer.data
        
    class Meta:
        model = Routes
        fields = ('__all__')

class Route_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Route_Types
        fields = ('__all__')

class Route_Type_Rules_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Route_Type_Rules
        fields = ('__all__')