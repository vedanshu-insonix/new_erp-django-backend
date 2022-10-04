from ..models.common import *
from ..models.columns import App, Columns
from rest_framework import serializers
from rest_framework.response import Response
from .user_serializers import RelatedUserSerilaizer


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

# ************************ Country Serializer ******************************************
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
        currency = RelatedCurrencySerializer(instance.currency).data
        if 'id' in currency:
            response['currency'] = RelatedCurrencySerializer(instance.currency).data
            
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response

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

# ************************ Stage Serializer ******************************************    
class RelatedStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        exclude = ("created_time","modified_time","created_by")
        
class StageSerializer(serializers.ModelSerializer):
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
 
# ************************ App Serializer ******************************************

class RelatedAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        exclude = ("created_time","modified_time","created_by")

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
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

# ************************ Configuration Serializer ******************************************    
class ConfigurationSerializer(serializers.ModelSerializer):
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
        
        application = RelatedAppSerializer(instance.application).data
        if 'id' in application:
            response['application'] = RelatedAppSerializer(instance.application).data
            
        return response

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

# ********************** Fields Serilaizer ***********************************************
class RelatedFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("__all__") 
        exclude = ("created_time","modified_time","created_by")
        
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("__all__") 
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        app_data = RelatedAppSerializer(instance.application).data
        if 'id' in app_data:
            response['application'] = RelatedAppSerializer(instance.application).data
            
        form_data = RelatedFormSerializer(instance.form).data
        if 'id' in form_data:
            response['form'] = RelatedFormSerializer(instance.form).data
        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        return response

# ************************ Choice Serializer ******************************************
class RelatedChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ("created_time","modified_time","created_by")
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("__all__") 
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
            
        application = RelatedAppSerializer(instance.application).data
        if 'id' in application:
            response['application'] = RelatedAppSerializer(instance.application).data
            
        field = RelatedFieldSerializer(instance.field).data
        if 'id' in field:
            response['field'] = RelatedFieldSerializer(instance.field).data
        return response

# ************************ List Serializer ****************************************** 
class RelatedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        exclude = ("created_time","modified_time","created_by")
 
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
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
    class Meta:
        model = Columns
        exclude = ("created_time","modified_time","created_by")

class ColumnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columns
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        app_data = RelatedAppSerializer(instance.app).data
        
        if 'id' in app_data:
            response['app'] = RelatedAppSerializer(instance.app).data
            
        list_data = RelatedListSerializer(instance.list).data
        if 'id' in list_data:
            response['list'] = RelatedListSerializer(instance.list).data
        return response 

# ************************ Menu Serializer ******************************************
class RelatedMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ("created_time","modified_time","created_by")
         
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    # To return forign key values in detail
    def to_representation(self, instance):
        response = super().to_representation(instance)
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        
        list_data = RelatedListSerializer(instance.list).data
        if 'id' in list_data:
            response['list'] = RelatedListSerializer(instance.list).data
            
        return response


# ************************ Form Serializer ******************************************  
class RelatedFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ("created_time","modified_time","created_by")
   
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        menu_data = RelatedMenuSerializer(instance.menu).data
        if 'id' in menu_data:
            response['menu'] = RelatedMenuSerializer(instance.menu).data
            
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response 

class FormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormList
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        form = RelatedFormSerializer(instance.form).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form).data
            
        list = RelatedListSerializer(instance.list).data
        if 'id' in list:
            response['list'] = RelatedListSerializer(instance.list).data
            
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response


class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = ("__all__")
        read_only_fields = ("created_time", "modified_time")
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def to_representation(self, instance):
        response = super().to_representation(instance)
        form = RelatedFormSerializer(instance.form).data
        if 'id' in form:
            response['form'] = RelatedFormSerializer(instance.form).data
                        
        created_by = RelatedUserSerilaizer(instance.created_by).data
        if 'id' in created_by:
            response['created_by'] = RelatedUserSerilaizer(instance.created_by).data
        return response

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

 
