from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.quotations import SalesQuotations
from sales.serializers.quotations_serializers import SalesQuotationsSerializer
from rest_framework.response import Response
from rest_framework import status



class SalesQuotationsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows quotations to be modified.
    """
    queryset = SalesQuotations.objects.all()
    serializer_class = SalesQuotationsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    def create(self,request):
        data = request.data
        try:
            if data['merchandise']:
                price = data['merchandise']
                cal_tax = (float(price)*10)/100
                data['tax'] = cal_tax
                total = float(price) + cal_tax + float(data.get('other')) + float(data.get('shipping'))
                data['total'] = total
                data['accepted_amount'] = total
            serializer = SalesQuotationsSerializer(data=data, context={'request': request})
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
            order_rec = SalesQuotations.objects.get(id=pk)
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
            serializer = SalesQuotationsSerializer(order_rec, data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            response = {'message': serializer.data,'status': 'success','code': status.HTTP_201_CREATED}
            return Response(response)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)