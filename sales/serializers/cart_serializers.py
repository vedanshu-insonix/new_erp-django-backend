from rest_framework import serializers
from sales.models.carts import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For Carts Model**************************#
class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='carts')
        if record_id:
            data['id']=get_rid_pkey('carts')
        return super().create(data)

#**************************Serializer For Cart Lines Model**************************#
class CartlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartlines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='cartlines')
        if record_id:
            data['id']=get_rid_pkey('cartlines')
        return super().create(data)