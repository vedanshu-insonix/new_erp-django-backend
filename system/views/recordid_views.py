from rest_framework import viewsets, filters
from ..serializers.recordid_serializers import *
from ..models.recordid import *
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from system import utils
# from .common_views import extracting_data

class RecordIdentifierViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Record ID to be modified.
    """
    queryset = RecordIdentifiers.objects.all()
    serializer_class = RecordIdentifierSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    # @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    # def import_data(self, request):
    #     try:
    #         file = request.FILES.get('file')
    #         if file:
    #             data_dict = extracting_data(file)
    #             count = 0
    #             for i in range(len(data_dict)):
    #                 record = data_dict[i]['record']
    #                 if record:
    #                     serializer=RecordIdentifierSerializer(data=data_dict[i], context={'request':request})
    #                     if serializer.is_valid(raise_exception=True):
    #                         serializer.save()
    #                         count += 1
    #             return Response(utils.success(count))
    #         else:
    #             msg="Please Upload A Suitable Excel File."
    #             return Response(utils.error(msg))
    #     except Exception as e:
    #         return Response(utils.error(str(e)))