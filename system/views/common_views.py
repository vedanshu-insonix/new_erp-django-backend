from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializers import *
from ..models.columns import App, Columns
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class ButtonViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Currency to be modified.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
           
class TagViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Tag to be modified.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class LanguageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Language to be modified.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class CountryViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        
class StateViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows State to be modified.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class StageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Stage to be modified.
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
       
class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Configuration to be modified.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        

class TerritoriesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Territories to be modified.
    """
    queryset = Territories.objects.all()
    serializer_class = TerritoriesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        
class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Choice to be modified.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class AppViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows App to be modified.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class FormViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Form to be modified.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class FieldViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Field to be modified.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
            'application__name': ['exact', 'contains'],
            'form__title':['exact', 'contains'],
            'application': ['exact'],
            'form': ['exact'],
            'field':['exact', 'contains'],
            'name':  ['exact', 'contains'],
            'type':  ['exact', 'contains'],
            'panel':  ['exact'],
            'position': ['exact']
            }
    ordering_fields = ("__all__")

class ListViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows List to be modified.
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
    # Related List 
    @action(detail=True, methods=['get'], url_path = "columns")
    def get_addresses(self, request, pk=None): 
        queryset = Columns.objects.filter(list = pk) 
        serializer = ColumnsSerializer(queryset, many = True)         
        return Response(serializer.data)
    
class ColumnsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Columns to be modified.
    """
    queryset = Columns.objects.all()
    serializer_class = ColumnsSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("app__name",)
    filterset_fields = {
            'app__name': ['exact','contains'],'list': ['exact'],'column': ['exact', 'contains'],
            'position': ['exact'],'default': ['exact'],
            'required': ['exact'],'optional': ['exact'],
        }
    ordering_fields = ("__all__")
    
         
class MenuViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ("__all__")
    filterset_fields = {
        'menu_category': ['exact', 'contains'],
        'list': ['exact'],
        'sequence': ['exact']
    }
    ordering_fields = ("__all__")
   
class HelpViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class FormListViewSet(viewsets.ModelViewSet):
    queryset = FormList.objects.all()
    serializer_class = FormListSerializer

class FormDataViewSet(viewsets.ModelViewSet):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer