from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from sales.models.quotations import SalesQuotations
from sales.serializers.quotations_serializers import SalesQuotationsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string

# To generate a unique id to reference an order/quotation other than pkey
def create_unique_id(title):
    unique_code = get_random_string(6, allowed_chars='0123456789')
    unique_code=f'{title}{unique_code}'
    return unique_code

class SalesQuotationsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows quotations to be modified.
    """
    queryset = SalesQuotations.objects.all()
    serializer_class = SalesQuotationsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    # Create
    def create(self,request):
        data = request.data
        try:
            new=False
            quotation_id=create_unique_id('SQ')
            while (new == False):
                check = SalesQuotations.objects.filter(quotation_id=quotation_id)
                if check:
                    quotation_id=create_unique_id('SQ')
                else:
                    new = True
            data['quotation_id'] = quotation_id
            if data['merchandise']:
                price = data['merchandise']
                tax_percent = data['tax']
                cal_tax = (float(price)*float(tax_percent))/100
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

    # Update
    def update(self,request,pk):
        data = request.data
        try:
            order_rec = SalesQuotations.objects.get(id=pk)
            if 'quotation_id' in data:
                result = "Quotation ID can't get updated."
            else:
                if 'merchandise' in data:
                    price = data['merchandise']
                else:
                    price = order_rec.merchandise
                serializer = SalesQuotationsSerializer(order_rec, data=data, context={'request': request}, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                result = serializer.data
            response = {'message': result,'status': 'success','code': status.HTTP_201_CREATED}
            return Response(response)
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)