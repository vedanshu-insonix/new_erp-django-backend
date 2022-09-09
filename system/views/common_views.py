from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializer import *

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
    permission_classes = [permissions.IsAuthenticated]
    

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Currency to be modified.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class TagViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Tag to be modified.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class LanguageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Language to be modified.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class CountryViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]
    

class StateViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

class StageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class TerritoriesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Territories.objects.all()
    serializer_class = TerritoriesSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class FieldViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class ListViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class MenuViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class FormViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated]


class HelpViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    permission_classes = [permissions.IsAuthenticated]
