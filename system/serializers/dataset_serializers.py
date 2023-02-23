from rest_framework import serializers
from system.models.dataset import Table, Data
from system.serializers.user_serializers import RelatedUserSerilaizer
from ..models.users import get_current_user_language
from ..models.translations import TranslationData
from system.serializers.common_serializers import  RelatedTranslationSerializer
from system.models.translations import Translation

class TableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        table_id = obj.id
        data_queryset = Data.objects.filter(table = table_id)
        serializer = DataSerializer(data_queryset, many = True)         
        return serializer.data
        
    class Meta:
        model = Table
        fields =("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 

    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

class DataSerializer(serializers.ModelSerializer):
    
    label = serializers.SerializerMethodField()
       
    def get_label(self, obj):
        data = obj.id
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationData.objects.filter(name = obj.id, translation__language__name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Data
        exclude =("created_time", "modified_time", "created_by")