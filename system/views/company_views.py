from rest_framework import viewsets
from ..serializers.company_serializers import *
from ..models.company import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from system import utils
from sales.serializers.addresses_serializers import AddressSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Company to be modified.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self, request):
        try:
            data=request.data
            haveBAddr=False
            haveSAddr=False
            haveUser=False
            if "billing_address" in data:
                billing_address= data.pop('billing_address')
                haveBAddr=True
            if "shipping_address" in data:
                shipping_address= data.pop('shipping_address')
                haveSAddr=True
            if "users" in data:
                user_detail = data.pop('users')
                haveUser=True
            serializer=CompanySerializer(data=data, context={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save
            company_id = serializer.data.get('id')
            if haveBAddr == True:
                if 'id' in billing_address:
                    CompanyAddress.objects.create(address=billing_address.get('id'),company=company_id)
                else:
                    new_address = AddressSerializer(data=billing_address, context={'request':request})
                    if new_address.is_valid(raise_exception=True):
                        new_address.save()
                    address_id=new_address.data.get('id')
                    create_company_address=CompanyAddress.objects.create(address=address_id,company=company_id)
            if haveSAddr == True:
                if 'id' in shipping_address:
                    CompanyAddress.objects.create(address=shipping_address.get('id'),company=company_id)
                else:
                    new_address = AddressSerializer(data=shipping_address, context={'request':request})
                    if new_address.is_valid(raise_exception=True):
                        new_address.save()
                    address_id=new_address.data.get('id')
                    create_company_address=CompanyAddress.objects.create(address=address_id,company=company_id)
            if haveUser == True:
                create_company_user=CompanyUser.objects.create(user=user_detail, company=company_id)
            company_rec=Company.objects.get(id=company_id)
            result=CompanySerializer(company_rec, context={'request':request})
            return Response(utils.success_msg(self,result.data))
        except Exception as e:
            return Response(utils.error(self,str(e)))