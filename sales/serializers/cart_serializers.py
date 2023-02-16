from rest_framework import serializers
from sales.models.carts import *
from system.service import get_primary_key
from system.models.recordid import RecordIdentifiers


class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Carts')
        if record_id:
            data['id']=get_primary_key('Carts')
        return data

class CartlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartlines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='Cartlines')
        if record_id:
            data['id']=get_primary_key('Cartlines')
        return data