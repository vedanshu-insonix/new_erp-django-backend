from rest_framework import viewsets
from warehouse.models.ledger import *
from warehouse.serializers.ledger_serializer import AccountsSerializer

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer