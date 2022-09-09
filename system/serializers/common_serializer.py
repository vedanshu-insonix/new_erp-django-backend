from ..models.common import *
from rest_framework import serializers



class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ("__all__")
    
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("__all__")
        
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("__all__")     
        
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("__all__")     
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("__all__")
        

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("__all__")
        

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ("__all__") 
        

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ("__all__")
        

class TerritoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Territories
        fields = ("__all__") 
        
        
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("__all__") 
        
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("__all__") 
        
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ("__all__")
        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("__all__")
        
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ("__all__")
        
class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ("__all__")
        
        

    
 
