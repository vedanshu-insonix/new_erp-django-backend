from rest_framework import serializers
from warehouse.models.shipping_models import *
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers
from system.models.users import get_current_user_language
from system.models.translations import TranslationContainerType
from system.serializers.common_serializers import RelatedTranslationSerializer
from system.models import Translation

#**************************Serializer For Deliveries Model**************************#
class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='deliveries')
        if record_id:
            data['id']=get_rid_pkey('deliveries')
        return super().create(data)

#**************************Serializer For Delivery Lines Model**************************#
class DeliveryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLines
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='deliverylines')
        if record_id:
            data['id']=get_rid_pkey('deliverylines')
        return super().create(data)

#**************************Serializer For Shipments Model**************************#
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='shipments')
        if record_id:
            data['id']=get_rid_pkey('shipments')
        return super().create(data)

#**************************Serializer For Container Types Model**************************#
class ContainerTypesSerializer(serializers.ModelSerializer):
    label=serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.id
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationContainerType.objects.filter(containerType = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = ContainerTypes
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='containertypes')
        if record_id:
            data['id']=get_rid_pkey('containertypes')
        return super().create(data)

#**************************Serializer For Containers Model**************************#
class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='containers')
        if record_id:
            data['id']=get_rid_pkey('containers')
        return super().create(data)

#**************************Serializer For Contents Model**************************#
class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ('__all__')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='contents')
        if record_id:
            data['id']=get_rid_pkey('contents')
        return super().create(data)