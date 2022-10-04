from django.shortcuts import render
from rest_framework import viewsets
from ..models.customers import Customer, CustomerAddress
from ..models.address import Address
from ..serializers.customers_serializers import CustomerSerializer
from ..serializers.addresses_serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Customers to be modified.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ("__all__")
    filterset_fields = {
            'name': ['exact', 'contains'],'entity': ['exact', 'contains'],'shipping_terms': ['exact', 'contains'],
            'ship_via': ['exact', 'contains'],'source': ['exact', 'contains'],'payment_terms': ['exact', 'contains'],'payment_method': ['exact', 'contains'],
            'sales_currency' : ['exact'],'free_freight_min' : ['exact', 'contains'],'issue_statements' : ['exact'],
            'require_pos': ['exact'],'credit_limit': ['exact', 'contains'],'account_balance': ['exact', 'contains'],
            'current_orders': ['exact', 'contains'], 'authorised_card': ['exact', 'contains'], 'credit_avail': ['exact', 'contains'],
            'overdue': ['exact'],'avg_pay_days': ['exact'],'last_credit_review': ['exact'],'credit_hold': ['exact'],
            'account_receivable': ['exact'],'stage': ['exact'],'stage_started': ['exact'],'status': ['exact'], 'used': ['exact']
        }
    ordering_fields = ("__all__")
    
    # Related List 
    @action(detail=True, methods=['get'], url_path = "addresses")
    def get_addresses(self, request, pk=None): 
        queryset = CustomerAddress.objects.filter(customer = pk)
        address_ids = []
        for ele in queryset:
            address_ids.append(ele.address.id)
        address_queryset = Address.objects.filter(id__in = address_ids)  
        serializer = AddressSerializer(address_queryset, many = True)         
        return Response(serializer.data)
