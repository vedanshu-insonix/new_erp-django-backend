from rest_framework import serializers
from ..models.translations import *
from ..serializers.user_serializers import RelatedUserSerilaizer
from ..serializers.common_serializers import RelatedLanguageSerializer


class TranslationSerializer(serializers.ModelSerializer):
    column = serializers.SerializerMethodField()
    formdata = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()
    help = serializers.SerializerMethodField()
    button = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    tile = serializers.SerializerMethodField()
    
    class Meta:
        model = Translation
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        language = RelatedLanguageSerializer(instance.language).data
        if 'id' in language:
            response['language'] = RelatedLanguageSerializer(instance.language).data
            
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response