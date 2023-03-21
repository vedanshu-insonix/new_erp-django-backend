from secrets import choice
from ..models.common import *
from ..models.translations import *
from ..models.columns import Column
from rest_framework import serializers
from .user_serializers import RelatedUserSerilaizer
from ..models.translations import TranslationFromData
from ..models.users import get_current_user_language
from system import utils
from django.db.models import Q
from system.service import get_rid_pkey, get_related_pkey
from system.models.recordid import RecordIdentifiers
from system.models.dataset import Data
#from .dataset_serializers import RelatedDataSerializer

# ************************ Button Serializer ******************************************

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='button')
        if record_id:
            data['id']=get_rid_pkey('button')
        return super().create(data)
        
# ************************ Button Serializer ******************************************
class RelatedCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ("created_time", "modified_time", "created_by")
        
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='currency')
        if record_id:
            data['id']=get_rid_pkey('currency')
        return super().create(data)
       
# ************************ Tag Serializer ******************************************             
class RelatedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ("created_time", "modified_time", "created_by")
                     
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("__all__") 
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='tag')
        if record_id:
            data['id']=get_rid_pkey('tag')
        return super().create(data)

# ************************ Language Serializer ******************************************
class RelatedLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ("created_time", "modified_time", "created_by") 
      
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='language')
        if record_id:
            data['id']=get_rid_pkey('language')
        return super().create(data)

# *********************** Country Serializer *****************************************
class RelatedCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ("created_time", "modified_time", "created_by") 
  
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return foreign key values in details
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='country')
        if record_id:
            data['id']=get_rid_pkey('country')
        return super().create(data)

# ************************ State Serializer ******************************************
class RelatedStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        exclude = ("created_time","modified_time","created_by")
  
class StateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = State
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        country = RelatedCountrySerializer(instance.country).data
        if 'id' in country:
            response['country'] = RelatedCountrySerializer(instance.country).data
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response
    
    def create(self, data):
        country = data['country']
        country_id=Country.objects.get(country__name=country)
        sequence = data['sequence']
        data['id']=get_related_pkey('state', country_id.id, sequence)
        return super().create(data)

#******************************* Stage Action Serializer *******************************

class RelatedStageActionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.action
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationStageAction.objects.filter(stage_action = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = StageAction
        exclude = ("created_time","modified_time","created_by", "stage")

class StageActionSerializer(serializers.ModelSerializer): 
    action = serializers.CharField(max_length = 255, required = True)
    class Meta:
        model = StageAction
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 

# ************************ Stage Serializer ******************************************    
class RelatedStageSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationStage.objects.filter(stage = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Stage
        exclude = ("created_time","modified_time","created_by")

class StageSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField()
    stage_actions = serializers.SerializerMethodField()
    
    def get_stage_actions(self, obj):
        request = self.context['request']
        stage_actions = StageAction.objects.filter()
        serializers = RelatedStageActionSerializer(stage_actions, many = True, context={'request': request})
        return serializers.data
    
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationStage.objects.filter(stage = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
        
    class Meta:
        model = Stage
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}} 
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='stage')
        if record_id:
            data['id']=get_rid_pkey('stage')
        return super().create(data)
     
# ************************ Configuration Serializer ******************************************    
class RelatedConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        exclude = ("created_time","modified_time","created_by")
        
class ConfigurationSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.id
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationConfiguration.objects.filter(configuration = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Configuration
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
                    
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='configuration')
        if record_id:
            data['id']=get_rid_pkey('configuration')
        return super().create(data)
    
# ************************ Territories Serializer ******************************************  
class RelatedTerritoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territories
        exclude = ("created_time","modified_time","created_by")
    
class TerritoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territories
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='territories')
        if record_id:
            data['id']=get_rid_pkey('territories')
        return super().create(data)

# ********************** Fields Serilaizer ***********************************************
# class RelatedFieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Field
#         fields = ("__all__") 
#         exclude = ("created_time","modified_time","created_by")
        
# class FieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Field
#         fields = ("__all__") 
#         read_only_fields = ("created_time", "modified_time")
#         extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         app_data = RelatedAppSerializer(instance.application).data
#         if 'id' in app_data:
#             response['application'] = RelatedAppSerializer(instance.application).data
            
#         form_data = RelatedFormSerializer(instance.form).data
#         if 'id' in form_data:
#             response['form'] = RelatedFormSerializer(instance.form).data
        
#         created_by = RelatedUserSerilaizer(instance.created_by).data
#         if 'id' in created_by:
#             response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
#         return response

# ************************ Selector Serializer ******************************************
class SelectorSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.id
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationSelector.objects.filter(selector = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Selectors
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
                    
        return response
    
    def validate(self, data):
        selector = data.get('system_name')
        data['system_name'] = utils.encode_api_name(selector)
        return data
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='selectors')
        if record_id:
            data['id']=get_rid_pkey('selectors')
        return super().create(data)
    
# ************************ Choice Serializer ******************************************
class RelatedChoiceSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
       
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationChoice.objects.filter(choice = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    
    
    class Meta:
        model = Choice
        fields = ("id","system_name","label")
        
class ChoiceSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationChoice.objects.filter(choice = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    
    class Meta:
        model = Choice
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
                    
        system_name = instance.system_name
        if system_name:
            response['system_name'] = utils.decode_api_name(system_name)   
        
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data

        request = self.context['request']
        
        return response

    def create(self, data):
        selector = data['selector']
        sel_id=Selectors.objects.get(system_name=selector)
        sequence = data['sequence']
        data['id']=get_related_pkey('choice', sel_id.id, sequence)
        return super().create(data)
    
# ************************ List Serializer ****************************************** 
class RelatedListSerializer(serializers.ModelSerializer):
    columns = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationList.objects.filter(list = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
        
    def get_columns(self, obj):
        request = self.context['request']
        list_id = obj.id
        list_queryset = Column.objects.filter(col_list = list_id).order_by('position')
        serializer = RelatedColumnsSerializer(list_queryset, many = True, context={'request': request})         
        return serializer.data
    
    def get_icon(self,obj):
        list = obj.id
        if list:
            queryset = ListIcon.objects.filter(list = list).first()
            serializers = ListIconSerializer(queryset, many=False)
            return serializers.data['icon'] 
        return None  
        
    class Meta:
        model = List
        exclude = ("created_time","modified_time","created_by")
    
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        data_source = instance.data_source
        if data_source:
            response['data_source'] = instance.data_source.system_name
        return response
    
class ListSerializer(serializers.ModelSerializer):
    system_name = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField()
    columns = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationList.objects.filter(list = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
        
    def get_columns(self, obj):
        request = self.context['request']
        list_id = obj.id
        list_queryset = Column.objects.filter(col_list = list_id).order_by('position')
        serializer = RelatedColumnsSerializer(list_queryset, many = True, context={'request': request})         
        return serializer.data
    
    class Meta:
        model = List
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        data_source = instance.data_source
        if data_source:
            response['data_source'] = instance.data_source.system_name        
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='list')
        if record_id:
            data['id']=get_rid_pkey('list')
        return super().create(data)

class ListFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListFilters
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='listfilters')
        if record_id:
            data['id']=get_rid_pkey('listfilters')
        return super().create(data)

class ListIconSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(max_length = 255, required = True)
    class Meta:
        model = ListIcon
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

# ************************ Columns Serializer ****************************************** 
class RelatedColumnsSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.column
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationColumn.objects.filter(column = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Column
        exclude = ("created_time","modified_time","created_by","col_list")
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        visibility = instance.visibility
        if visibility:
            response['visibility'] = instance.visibility.system_name
        return response
## column serializer
class ColumnsSerializer(serializers.ModelSerializer):
    column = serializers.CharField(max_length = 255, required = True)
    field = serializers.CharField(max_length = 255, required = True)
    label = serializers.SerializerMethodField() 
    def get_label(self, obj):
        data = obj.column
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationColumn.objects.filter(column = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Column
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        list_data = RelatedListSerializer(instance.col_list, context={'request': request}).data        
        if 'id' in list_data:
            data = RelatedListSerializer(instance.col_list, context={'request': request}).data
            list = data.pop('columns')
            response['col_list'] = data
        visibility = instance.visibility
        if visibility:
            response['visibility'] = instance.visibility.system_name
        
        
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='column')
        if record_id:
            data['id']=get_rid_pkey('column')
        return super().create(data)

# ************************ Menu Serializer ******************************************
class RelatedMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ("created_time","modified_time","created_by")
         
class MenuSerializer(serializers.ModelSerializer):
    form = serializers.SerializerMethodField()
    
    def get_form(self, obj):
        request = self.context['request']
        list_details = obj.list
        if list_details != None:
            list_id = list_details.id
            formlist = FormList.objects.filter(Q(relation = "Parent") | Q(relation = "parent"), list__id = list_id).first()
            serializers = FormListSerializer(formlist, many= False, context={'request': request})
            if serializers.data:
                return serializers.data['form']
            return serializers.data
        return None
    class Meta:
        model = Menu
        exclude = ('created_time', 'modified_time', 'created_by', 'description')
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        list_data = RelatedListSerializer(instance.list, context={'request': request}).data
        if 'id' in list_data:
            response['list'] = RelatedListSerializer(instance.list, context={'request': request}).data
        menu_category = instance.menu_category
        if menu_category:
            response['menu_category']=instance.menu_category.system_name
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='menu')
        if record_id:
            data['id']=get_rid_pkey('menu')
        return super().create(data)


# ************************ Form Serializer ******************************************  
class RelatedFormSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationForm.objects.filter(form = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Form
        exclude = ("created_time","modified_time","created_by")
   
class FormSerializer(serializers.ModelSerializer):
    form_list = serializers.SerializerMethodField()
    form_data = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    # icons = serializers.SerializerMethodField()

    def get_form_list(self,obj):
        request = self.context['request']
        form_list = FormList.objects.filter(form = obj.id).order_by('position')
        serializer = RelatedFormListSerializer(form_list, many = True, context={'request': request})
        return serializer.data
    
    def get_form_data(self,obj):
        request = self.context['request']
        form_data = FormData.objects.filter(form = obj.id).order_by('position')
        serializer = RelatedFormDataSerializer(form_data, many = True, context={'request': request})  
        return serializer.data
    
    def get_label(self, obj):
        data = obj.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationForm.objects.filter(form = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    
    def get_section(self,obj):
        request = self.context['request']
        form_section = FormSection.objects.filter(form = obj.id).order_by('section_sequence')
        serializer = RelatedFormSectionSerializer(form_section, many = True, context={'request': request})  
        return serializer.data
    
    # def get_icons(self,obj):
    #     request = self.context['request']
    #     form_icons = FormIcon.objects.filter(form = obj.id)
    #     serializer = FormIconSerializer(form_icons, many = True, context={'request': request})  
    #     return serializer.data

    class Meta:
        model = Form
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        request = self.context['request']
        base = request.build_absolute_uri('/')
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        icons = instance.icon
        if icons:
            response['icon']=base+str(instance.icon.icon_image)
        request = self.context['request']
        return response

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='form')
        if record_id:
            data['id']=get_rid_pkey('form')
        return super().create(data)

class RelatedFormListSerializer(serializers.ModelSerializer):  
    icon = serializers.SerializerMethodField()
    display_records = serializers.SerializerMethodField()
    def get_icon(self,obj):
        list = obj.list
        request = self.context['request']
        if list:
            queryset = ListIcon.objects.filter(list = obj.list.id).first()
            serializers = ListIconSerializer(queryset, many=False, context={'request':request})
            return serializers.data['icon'] 
        return None  
        
    def get_display_records(self,obj):
        list = obj.list
        request = self.context['request']
        if list:
            queryset = Configuration.objects.filter(system_name = list)
            serializers = RelatedConfigurationSerializer(queryset , many = False, context={'request':request})
            return {"current_value": serializers.data['current_value'],
                    "default_value": serializers.data['default_value']}
        return None
     
    class Meta:
        model = FormList
        exclude = ("created_time", "modified_time","form","created_by")
      
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        list = RelatedListSerializer(instance.list, context={'request':request}).data
        if 'id' in list:
            response['list'] = RelatedListSerializer(instance.list, context={'request': request}).data
        return response

class FormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormList
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        form = RelatedFormSerializer(instance.form, context={'request': request}).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form, context={'request': request}).data
            
        list = RelatedListSerializer(instance.list, context={'request': request}).data
        if 'id' in list:
            response['list'] = RelatedListSerializer(instance.list, context={'request': request}).data
            
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='formlist')
        if record_id:
            data['id']=get_rid_pkey('formlist')
        return super().create(data)

class RelatedTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ("id","label")

class RelatedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        exclude =("created_time", "modified_time", "created_by", "data_source")
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        base = request.build_absolute_uri('/') + 'api/'

        field = instance.field
        field_type = instance.field_type
        if field_type:
            field_type = instance.field_type.system_name
            response['field_type']= instance.field_type.system_name



        if field and field_type=='dropdown':
            if field == 'State' or field == 'state':
                add_link = 'states/?country='
                link = base+add_link
                response['link'] = link
            elif field == 'Country' or field == 'country':
                add_link = 'countries/'
                link = base+add_link
                response['link'] = link
                response['child_field'] = 'state'
            elif field == 'Language' or field == 'language':
                add_link = 'languages/'
                link = base+add_link
                response['link'] = link
            elif field == 'Stage' or field == 'stage':
                add_link = 'stages/?form='
                link = base+add_link
                response['link'] = link
            elif 'currency'in field or 'Currency' in field:
                add_link = 'currencies/'
                link = base+add_link
                response['link'] = link
            elif 'list' in field or 'List' in field:
                add_link = 'lists/'
                link = base+add_link
                response['link'] = link
            elif 'form' in field or 'Form' in field:
                add_link = 'forms/'
                link = base+add_link
                response['link'] = link
            elif 'column' in field or 'Column' in field:
                add_link = 'columns/'
                link = base+add_link
                response['link'] = link
            else:
                sel_id = Selectors.objects.filter(system_name=field)
                if sel_id:
                    add_link = 'choices/?selector='+sel_id.values()[0]['id']
                    link = base+add_link
                    response['link'] = link
        return response 
        
class RelatedFormDataSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    default = serializers.SerializerMethodField()
    # choices = serializers.SerializerMethodField()
    
    # def get_choices(self, obj):
    #     field = obj.field
    #     request = self.context['request']
    #     return None
    
    def get_label(self, obj):
        data = obj.data
        if data:
            data = obj.data.system_name
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationFromData.objects.filter(formdata = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    
    def get_default(self,obj):
        data = obj.data
        if data:
            data = obj.data.system_name
        queryset = Configuration.objects.filter(system_name = data).first()
        serializers = RelatedConfigurationSerializer(queryset, many = False)
        return serializers.data['default_value']
    
    class Meta:
        model = FormData
        exclude = ("created_time", "modified_time",'form', 'created_by')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
        data = instance.data

        section = RelatedFormSectionSerializer(instance.section, context={'request':request}).data
        if 'id' in section:
            response['section'] = RelatedFormSectionSerializer(instance.section, context={'request':request}).data


        data = RelatedDataSerializer(instance.data, context={'request':request}).data
        if 'id' in data:
            response['data'] = RelatedDataSerializer(instance.data, context={'request':request}).data
            # response['section'] = RelatedFormSectionSerializer(instance.section, context={'request':request}).data


        # data = RelatedDataSerializer(instance.data).data
        # if 'id' in data:
        #     response['data'] = RelatedDataSerializer(instance.data, context={'request':request}).data

        # field = instance.field
        # field_type = instance.type
        # if field and field_type=='dropdown':
        #     if field == 'State' or field == 'state':
        #         add_link = 'states/?country='
        #         link = base+add_link
        #         response['link'] = link
        #     elif field == 'Country' or field == 'country':
        #         add_link = 'countries/'
        #         link = base+add_link
        #         response['link'] = link
        #         response['child_field'] = 'state'
        #     elif field == 'Language' or field == 'language':
        #         add_link = 'languages/'
        #         link = base+add_link
        #         response['link'] = link
        #     elif field == 'Stage' or field == 'stage':
        #         add_link = 'stages/?form='
        #         link = base+add_link
        #         response['link'] = link
        #     elif 'currency'in field or 'Currency' in field:
        #         add_link = 'currencies/'
        #         link = base+add_link
        #         response['link'] = link
        #     elif 'list' in field or 'List' in field:
        #         add_link = 'lists/'
        #         link = base+add_link
        #         response['link'] = link
        #     elif 'form' in field or 'Form' in field:
        #         add_link = 'forms/'
        #         link = base+add_link
        #         response['link'] = link
        #     elif 'column' in field or 'Column' in field:
        #         add_link = 'columns/'
        #         link = base+add_link
        #         response['link'] = link
        #     else:
        #         sel_id = Selectors.objects.filter(system_name=field)
        #         if sel_id:
        #             add_link = 'choices/?selector='+sel_id.values()[0]['id']
        #             link = base+add_link
        #             response['link'] = link
        validations = {'datatype': response['data_type'], 'required': response['is_required']}
        if response['data_type']:
            datatype = ''.join(e.lower() for e in response['data_type'] if e.isalnum())

            if datatype == 'email' or 'website':
                validations['format'] = response['format']
            elif datatype == 'string':
                validations['min_length'] = response['minimum']
                validations['max_length'] = response['maximum']
            elif datatype == 'number':
                validations['min'] = response['minimum']
                validations['max'] = response['maximum']

        response['validations'] = validations
        table = instance.table
        if table:
            response['table'] = instance.table.system_name                       
        return response 

class FormDataSerializer(serializers.ModelSerializer):
    field = serializers.CharField(max_length= 255, required = True)
    class Meta:
        model = FormData
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        request = self.context['request']
                    
        form = RelatedFormSerializer(instance.form, context={'request': request}).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form, context={'request': request}).data
        data = instance.data
        if data:
            response['data'] = instance.data.system_name
        table = instance.table
        if table:
            response['table'] = instance.table.system_name             
                     
                     
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data


        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='formdata')
        if record_id:
            data['id']=get_rid_pkey('formdata')
        return super().create(data)
    
# ************************ Help Serializer ****************************************** 
class RelatedHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        exclude = ("created_time","modified_time","created_by")
    
class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        form = RelatedFormSerializer(instance.form).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form).data
        
        stage = RelatedStageSerializer(instance.stage).data
        if 'id' in stage:
            response['stage'] = RelatedStageSerializer(instance.stage).data
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response
    
    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='help')
        if record_id:
            data['id']=get_rid_pkey('help')
        return super().create(data)

class RelatedFormSectionSerializer(serializers.ModelSerializer):
    section_title = serializers.CharField(required = True, max_length = 255)
    class Meta:
        model = FormSection
        exclude = ("created_time","modified_time","created_by", "form")

class IconSerializer(serializers.ModelSerializer):
    def get_label(self, obj):
        data = obj.data
        user = self.context['request'].user
        language = get_current_user_language(user)
        queryset = TranslationIcons.objects.filter(icon = obj.id, translation__language__system_name = language).first()
        if queryset:
            translation_id = queryset.translation.id
            translation= Translation.objects.filter(id = translation_id, language__system_name = language).first()
            serializers = RelatedTranslationSerializer(translation, many=False)
            return serializers.data['label']
        else:
            return data
    class Meta:
        model = Icons
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='icons')
        if record_id:
            data['id']=get_rid_pkey('icons')
        return super().create(data)

# ****************************** Action Serializer *********************************************************
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

    def create(self, data):
        record_id = RecordIdentifiers.objects.filter(record='action')
        if record_id:
            data['id']=get_rid_pkey('action')
        return super().create(data)
       
# ****************************** Form Stage Serializer *********************************************************
class FormStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormStage
        fields = ("__all__")
        
# ****************************** Button Stage Serializer *********************************************************
class ButtonStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonStage
        fields = ("__all__")