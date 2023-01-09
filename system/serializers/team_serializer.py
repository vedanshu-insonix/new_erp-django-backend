from ..models.company import *
from rest_framework import serializers
from system.models.teams import *

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("__all__")

class TeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRole
        fields = ("__all__")

class TeamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamUser
        fields = ("__all__")