from rest_framework import serializers
from system.models.dataset import DataTable, Data, DataRequirements
from system.models import Translation
from ..models.users import get_current_user_language
from system.serializers.common_serializers import RelatedTranslationSerializer, RelatedFormSerializer, RelatedStageSerializer, RelatedChoiceSerializer
from system.serializers.user_serializers import RelatedUserSerilaizer
from system.service import get_rid_pkey, get_related_pkey
from system.models.recordid import RecordIdentifiers

#**************************Serializer For DataTable Model**************************#
class TableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        table_id = obj.id
        request = self.context['request']
        data_queryset = Data.objects.filter(data_source = table_id)
        serializer = DataSerializer(data_queryset, many = True, context={'request':request})         
        return serializer.data
        
    class Meta:
        model = DataTable
        fields =("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)

        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='datatable')
        if record_id:
            data['id']=get_rid_pkey('datatable')
        return super().create(data)

#**************************Serializer For Data Model**************************#
class RelatedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        exclude =("created_time", "modified_time", "created_by")

class DataSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = Translation.objects.filter(data = obj.id, language__system_name = language).first()
        if queryset:
            serializers = RelatedTranslationSerializer(queryset, many=False)
            return serializers.data['label']
        else:
            return data
    #     queryset = TranslationData.objects.filter(name = obj.id, translation__language__system_name = language).first()
    #     if queryset:
    #         translation_id = queryset.translation.id
    #         translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
    #         serializers = RelatedTranslationSerializer(translation, many=False)
    #         return serializers.data['label']
    #     else:
    #         return data
    class Meta:
        model = Data
        exclude =("created_time", "modified_time", "created_by")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        
        data_source = instance.data_source
        if data_source:
            response['data_source'] = instance.data_source.system_name
        linked_ds = instance.linked_ds
        if linked_ds:
            response['linked_ds'] = instance.linked_ds.system_name             
        linked_data = instance.linked_data
        if linked_data:
            response['linked_data'] = instance.linked_data.system_name 
                              
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        return response

    # pkey of new data will be created on the basis of recordidentifiers.
    def create(self, data):
        datasource = data['data_source']
        dataSource_id=DataTable.objects.get(id=datasource.id)
        sequence = data['sequence']
        data['id']=get_related_pkey('data', dataSource_id.id, sequence)
        return super().create(data)
    
#**************************Serializer For Data Requirements Model**************************#
class DataRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRequirements
        exclude =("created_time", "modified_time", "created_by")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']

        form = RelatedFormSerializer(instance.form, context={'request':request}).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form, context={'request':request}).data
        data = RelatedDataSerializer(instance.data, context={'request':request}).data
        if 'id' in data:
            response['data'] = RelatedDataSerializer(instance.data, context={'request':request}).data
        stage = RelatedStageSerializer(instance.stage, context={'request':request}).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage, context={'request':request}).data
        requirement = RelatedChoiceSerializer(instance.requirement, context={'request':request}).data
        if 'id' in requirement:
            response['requirement'] = RelatedChoiceSerializer(instance.requirement, context={'request':request}).data
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response