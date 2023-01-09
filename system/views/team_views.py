from rest_framework import viewsets
from system.models.teams import *
from system.serializers.team_serializer import *

class TeamViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Team to be modified.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamRoleViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamRole to be modified.
    """
    queryset = TeamRole.objects.all()
    serializer_class = TeamRoleSerializer

class TeamUserViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows TeamUser to be modified.
    """
    queryset = TeamUser.objects.all()
    serializer_class = TeamUserSerializer