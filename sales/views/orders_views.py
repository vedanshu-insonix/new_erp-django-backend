from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.sales_orders import SalesOrders, SalesOrderLines
from sales.serializers.orders_serializers import SalesOrdersSerializer, SalesOrderLinesSerializer
from rest_framework.response import Response
from rest_framework import status
from sales.views.quotations_views import create_unique_id

class SalesOrdersViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows orders to be modified.
    """
    queryset = SalesOrders.objects.all()
    serializer_class = SalesOrdersSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self,request):
        data = request.data
        try:
            new=False
            order_id=create_unique_id('SO')
            while (new == False):
                check = SalesOrders.objects.filter(order_id=order_id)
                if check:
                    order_id=create_unique_id('SO')
                else:
                    new = True
            data['order_id'] = order_id
            if data['merchandise']:
                price = data['merchandise']
                tax_percent = data['tax']
                cal_tax = (float(price)*float(tax_percent))/100
                data['tax'] = cal_tax
                total = float(price) + cal_tax + float(data.get('other')) + float(data.get('shipping'))
                data['total'] = total
                data['accepted_amount'] = total
            serializer = SalesOrdersSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            response = {'message': serializer.data,'status': 'success','code': status.HTTP_201_CREATED}
            return Response(response)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)

    def update(self,request,pk):
        data = request.data
        try:
            order_rec = SalesOrders.objects.get(id=pk)
            if 'merchandise' in data:
                price = data['merchandise']
                cal_tax = (float(price)*10)/100
                data['tax'] = cal_tax
                if 'other' in data:
                    other = data.get('other')
                else:
                    other = order_rec.other
                if 'shipping' in data:
                    shipping = data.get('shipping')
                else:
                    shipping = order_rec.shipping
                total = float(price) + cal_tax + float(other) + float(shipping)
                data['total'] = total
                data['accepted_amount'] = total
            serializer = SalesOrdersSerializer(order_rec, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            response = {'message': serializer.data,'status': 'success','code': status.HTTP_201_CREATED}
            return Response(response)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)

class SalesOrderLinesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows order lines to be modified.
    """
    queryset = SalesOrderLines.objects.all()
    serializer_class = SalesOrderLinesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")