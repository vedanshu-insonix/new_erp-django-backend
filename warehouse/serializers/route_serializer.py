from rest_framework import serializers
from warehouse.models.routes import *
from warehouse.models.operation import Operations
from warehouse.serializers.operation_serializer import Operation_Serializer
from system.service import get_rid_pkey
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
        record_id = RecordIdentifiers.objects.filter(record='routes')
        if record_id:
            data['id']=get_rid_pkey('routes')
        return data

class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTypes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='routetypes')
        if record_id:
            data['id']=get_rid_pkey('routetypes')
        return data

class RouteTypeRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteTypeRules
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='routetyperules')
        if record_id:
            data['id']=get_rid_pkey('routetyperules')
        return data