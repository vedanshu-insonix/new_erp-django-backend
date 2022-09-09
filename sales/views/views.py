from django.shortcuts import render
from rest_framework import viewsets
from ..models.customers import Customer
from ..models.vendors import Vendor
from ..serializers.serializers import *
from rest_framework import permissions
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class AddressViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Addresses to be modified.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class VendorViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Vendors to be modified.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]