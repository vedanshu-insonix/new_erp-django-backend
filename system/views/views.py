from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from sales.models.customers import Customer
from ..serializers.user_serializers import UserSerializer, GroupSerializer, CustomerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows users to be modified.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows groups to be modified.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows groups to be modified.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
