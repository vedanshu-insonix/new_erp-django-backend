from rest_framework import serializers
from warehouse.models.shipping_models import *

from system.models.users import get_current_user_language
from system.models.translations import TranslationContainerType
from system.serializers.common_serializers import  RelatedTranslationSerializer
from system.models.translations import Translation

class DeliveriesSerializer(serializers.ModelSerializer):
    class meta:
        model = Deliveries
        fields = ('__all__')

class DeliveryLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLines
        fields = ('__all__')

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ('__all__')

class ContainerTypesSerializer(serializers.ModelSerializer):
    
    def get_label(self, obj):
        data = obj.id
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationContainerType.objects.filter(containerType = obj.id, translation__language__name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = ContainerTypes
        fields = ('__all__')

class ContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Containers
        fields = ('__all__')

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ('__all__')