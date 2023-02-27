from rest_framework import serializers
from system.models.dataset import DataTable, Data

from ..models.users import get_current_user_language
from ..models.translations import TranslationData
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.service import get_rid_pkey, get_related_pkey
from system.models.recordid import RecordIdentifiers

class TableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        table_id = obj.id
        data_queryset = Data.objects.filter(data_source = table_id)
        serializer = DataSerializer(data_queryset, many = True)         
        return serializer.data
        
    class Meta:
        model = DataTable
        fields =("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def validate(self, data):
        record_id = RecordIdentifiers.objects.filter(record='datatable')
        if record_id:
            data['id']=get_rid_pkey('datatable')
        return data

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
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def validate(self, data):
        datasource = data['data_source']
        dataSource_id=DataTable.objects.get(id=datasource.id)
        sequence = data['sequence']
        data['id']=get_related_pkey('data', dataSource_id.id, sequence)
        return data