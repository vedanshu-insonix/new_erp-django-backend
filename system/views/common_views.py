from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializers import *
from ..models.columns import App, Columns
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
import os
import openpyxl


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class ButtonViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Buttons to be modified.
    """
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Currency to be modified.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
           
class TagViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Tag to be modified.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class LanguageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Language to be modified.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class CountryViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        
class StateViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows State to be modified.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class StageViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Stage to be modified.
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
       
class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Configuration to be modified.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        

class TerritoriesViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Territories to be modified.
    """
    queryset = Territories.objects.all()
    serializer_class = TerritoriesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
        
class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Choice to be modified.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class AppViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows App to be modified.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
class FormViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Form to be modified.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('data')
            user_id = str(request.user.id)
            defective_data = []
            count = 0
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    if row_data[0].lower() == 'title':
                        pass
                    else:
                        try:
                            menurec = Menu.objects.get(menu_category=row_data[1].lower())
                        except Exception as e:
                            print('ERROR: ', str(e))
                            defective_data.append(row_data[1])
                            pass
                        else:
                            if menurec:
                                try:
                                    formrec = Form.objects.get(title=row_data[0].lower())
                                    if formrec:
                                        pass
                                except Exception as e:
                                    Form.objects.create(title=row_data[0].lower(),menu_id=menurec.id,created_by_id=user_id)
                                    count += 1
                            
            return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'failed':f'menu matching query for {defective_data} does not exist',
                            'inserted':f'{count} records are inserted'
                            
                            })
        except Exception as e:
            return Response({
                            'error_msg':str(e),
                            'status':status.HTTP_400_BAD_REQUEST
                            })
    
class FieldViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Field to be modified.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
            'application__name': ['exact', 'contains'],
            'form__title':['exact', 'contains'],
            'application': ['exact'],
            'form': ['exact'],
            'field':['exact', 'contains'],
            'name':  ['exact', 'contains'],
            'type':  ['exact', 'contains'],
            'panel':  ['exact'],
            'position': ['exact']
            }
    ordering_fields = ("__all__")

class ListViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows List to be modified.
    """
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")
    
    # Related List 
    @action(detail=True, methods=['get'], url_path = "columns")
    def get_addresses(self, request, pk=None): 
        queryset = Columns.objects.filter(list = pk) 
        serializer = ColumnsSerializer(queryset, many = True)         
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            filename, filextension = os.path.splitext(str(file))
            if filextension == '.csv':
                # df_new = pd.read_csv(file)
                # data = pd.ExcelWriter(filename+'.xlsx')
                # df_new.to_excel(data, index=False)
                # data.save()
                pass
            else:
                if filextension == '.xlsx':
                    data = request.FILES.get('data')
                
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                defective_data = []
                row_count = 0
                succeed_count = 0
                for row in sheet.iter_rows():
                    row_data = []
                    row_count = row_count + 1
                    for cell in row:
                        row_data.append(cell.value)
                    if row_data[0].lower() == 'form' or row_data[0].lower() == 'list' or row_data[0].lower() == 'sequence':
                        pass
                    else:
                        form_data = row_data[0]
                        list_data = row_data[1]
                        sequence_data = row_data[2]
                        data_dict = {}
                        try:
                            form_instance = Form.objects.get(title = form_data)
                            data_dict['form'] = form_instance.id
                        except Exception as e:
                            defective_data.append([form_data])
                            continue
                          
                        if list_data:
                            data_dict['list'] = list_data
                        
                        if sequence_data:
                            data_dict['sequence'] = sequence_data
                        
                        list_serializers = ListSerializer(data=data_dict, context={'request': request})
                        if list_serializers.is_valid():
                            list_serializers.save()
                            print(list_serializers.data)
                        
                        succeed_count = succeed_count + 1
            if defective_data:
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(succeed_count)+" row(s) inserted successfully",
                             'failed':f'form matching query for {defective_data} does not exist'})
            else: 
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(succeed_count)+" row(s) inserted successfully"
                             })
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
       
        
class ColumnsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Columns to be modified.
    """
    queryset = Columns.objects.all()
    serializer_class = ColumnsSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("app__name",)
    filterset_fields = {
            'app__name': ['exact','contains'],'list': ['exact'],'column': ['exact', 'contains'],
            'position': ['exact'],'default': ['exact'],
            'required': ['exact'],'optional': ['exact'],
        }
    ordering_fields = ("__all__")
    
         
class MenuViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("__all__")
    filterset_fields = {
        'menu_category': ['exact', 'contains'],
        'list': ['exact'],
        'sequence': ['exact']
    }
    ordering_fields = ("__all__")
   
class HelpViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Country to be modified.
    """
    queryset = Help.objects.all()
    serializer_class = HelpSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class FormListViewSet(viewsets.ModelViewSet):
    queryset = FormList.objects.all()
    serializer_class = FormListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

class FormDataViewSet(viewsets.ModelViewSet):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")