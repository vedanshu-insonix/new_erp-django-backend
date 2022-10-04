from django.db import models
from .common import BaseContent
from system.models.common import *
from django.contrib.auth.models import User

class Team(BaseContent):
    name = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name
    
class TeamUser(BaseContent):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='TeamUser')
    
    def __str__(self):
        return self.team + self.user

class TeamRole(BaseContent):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
    role = models.ForeignKey('Role', on_delete= models.CASCADE, null=True)
    