from rest_framework import serializers
from ..models.translations import *
from ..serializers.user_serializers import RelatedUserSerilaizer
from ..serializers.common_serializers import RelatedLanguageSerializer
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey
from system.models.recordid import RecordIdentifiers
from system.service import get_rid_pkey


class TranslationSerializer(serializers.ModelSerializer):
    column = serializers.SerializerMethodField()
    formdata = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()
    help = serializers.SerializerMethodField()
    button = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    # tile = serializers.SerializerMethodField()
    
    def get_column(self, obj):
        
        return None
    
    def get_formdata(self, obj):
        return None
    
    def get_menu(self, obj):
        return None
    
    def get_choice(self, obj):
        return None

    def get_help(self, obj):
        return None

    def get_button(self, obj):
        return None
    
    def get_stage(self, obj):
        return None

    def get_tag(self, obj):
        return None
    
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
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='translation')
        if record_id:
            data['id']=get_rid_pkey('translation')
        return super().create(data)