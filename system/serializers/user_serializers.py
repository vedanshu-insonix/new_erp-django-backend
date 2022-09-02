from django.contrib.auth.models import User, Group
from sales.models.customers import Customer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("__all__")
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("__all__")