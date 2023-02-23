from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from system import utils
from .common_views import extracting_data
from system.models.dataset import DataTable, Data
from system.serializers.dataset_serializers import TableSerializer, DataSerializer

class TableViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Table to be modified.
    """
    queryset = DataTable.objects.all()
    serializer_class = TableSerializer

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                data_dict = extracting_data(file)
                count = 0
                for i in range(len(data_dict)):
                    dataset_id = data_dict[i]['id']
                    system_name = data_dict[i]['system_name']
                    if system_name:
                        serializer=TableSerializer(data=data_dict[i], context={'request':request})
                        if serializer.is_valid(raise_exception=True):
                            serializer.save(id=dataset_id)
                            count += 1
                return Response(utils.success(count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(msg))
        except Exception as e:
            return Response(utils.error(str(e)))

class DataViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Table to be modified.
    """
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                data_dict = extracting_data(file)
                count = 0
                for i in range(len(data_dict)):
                    table_name = data_dict[i]['data_source']
                    data = data_dict[i]['name']
                    if table_name:
                        search = DataTable.objects.filter(table=table_name)
                        if search:
                            data_dict[i]['table'] = search.values()[0]['id']
                            table_id = search.values()[0]['id']
                            find=Data.objects.filter(table=table_id, name=data_dict[i]['name'])
                            if not find:
                                serializer=DataSerializer(data=data_dict[i], context={'request':request})
                                if serializer.is_valid(raise_exception=True):
                                    serializer.save()
                                    count += 1    
                return Response(utils.success(count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(msg))
        except Exception as e:
            return Response(utils.error(str(e)))
        
    # def destroy(self, pk):
    #     print(pk)
    #     queryset = Data.objects.filter(data_id=pk)
    #     queryset.delete()
    #     return "Deletion Successful."