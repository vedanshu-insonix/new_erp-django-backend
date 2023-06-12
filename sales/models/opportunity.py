from django.db import models
from system.models.common import BaseStatus
from django.contrib.auth.models import User

class Opportunities(BaseStatus):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    team = models.ForeignKey('system.Team', on_delete=models.CASCADE, null=True, blank=True, related_name='opportunities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='opportunities')
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    value = models.DecimalField(max_digits=30,decimal_places=2,blank=True, default=0.0)