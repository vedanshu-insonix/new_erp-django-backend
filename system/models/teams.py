from django.db import models
from .common import BaseContent
from django.contrib.auth.models import User

class Team(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True)
    team_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_team_type')
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    responsibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_team_responsibility')
    user = models.ManyToManyField(User, blank=True, related_name='team')
    role = models.ManyToManyField('Role', blank=True, related_name='team')
    
    def __str__(self):
        return self.name
    
# class TeamUser(BaseContent):
#     team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='TeamUser')
#     team_responsibility = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    
#     def __str__(self):
#         return self.team + self.user

# class TeamRole(BaseContent):
#     team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
#     role = models.ForeignKey('Role', on_delete= models.CASCADE, null=True)
    