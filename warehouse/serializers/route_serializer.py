from rest_framework import serializers
from warehouse.models.routes import *
from warehouse.models.operation import Operations
from warehouse.serializers.operation_serializer import Operation_Serializer
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers

class RouteSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField()

    def get_steps(self, obj):
        queryset = Operations.objects.filter(route = obj.id)
        serializer = Operation_Serializer(queryset, many=True)
        return serializer.data
        
    class Meta:
        model = Routes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Routes')
        if record_id:
            data['id']=get_primary_key('Routes')
        return data

class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTypes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='RouteTypes')
        if record_id:
            data['id']=get_primary_key('RouteTypes')
        return data

class RouteTypeRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTypeRules
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='RouteTypeRules')
        if record_id:
            data['id']=get_primary_key('RouteTypeRules')
        return data