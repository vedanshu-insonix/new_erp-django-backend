from rest_framework import viewsets
from ..models.purchase import *
from ..serializers.purchase_serializers import DisbursementSerializer, PurchaseOrderLinesSerializer, PurchaseOrderSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderLinesViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderLines.objects.all()
    serializer_class = PurchaseOrderLinesSerializer

class DisbursementViewSet(viewsets.ModelViewSet):
    queryset = Disbursment.objects.all()
    serializer_class = DisbursementSerializer