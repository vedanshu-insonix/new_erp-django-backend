from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.vendors import Vendors, VendorProducts
from ..serializers.vendors_serializers import VendorProductsSerializer, VendorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class VendorViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Vendors to be modified.
    """
    queryset = Vendors.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    

# class VendorAddressViewSet(viewsets.ModelViewSet):
#     queryset = VendorAddress.objects.all()
#     serializer_class = VendorAddressSerializer

class VendorProductsViewSet(viewsets.ModelViewSet):
    queryset = VendorProducts.objects.all()
    serializer_class = VendorProductsSerializer