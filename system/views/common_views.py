from ast import For
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializers import *
from ..models.columns import App, Column
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
    
    def list(self, request, *args, **kwargs):
        queryset = Stage.objects.filter().all()
        serializers = StageSerializer(queryset, many = True, context = {"request": request})
        return super().list(request, *args, **kwargs)
    

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                defective_data=[]
                count=0
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    if row_data[0].lower() == 'application':
                        pass
                    else:
                        form_rec = None
                        try:
                            form_rec = Form.objects.get(form=row_data[1])
                        except Exception as e:
                            print('ERROR: ', str(e))
                            defective_data.append(row_data[0])
                            pass
                        if form_rec:
                            stage_rec = Stage.objects.filter(stage = row_data[3],application=row_data[0],form=form_rec.id)
                            if stage_rec:
                                defective_data.append(row_data[0])
                            else:
                                Stage.objects.create(application=row_data[0], form=form_rec, sequence=row_data[2],stage=row_data[3], created_by_id=user_id)
                                count = count+1
            if defective_data:
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(count)+" row(s) inserted successfully",
                             'failed':f'{defective_data}'})
            else: 
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(count)+" row(s) inserted successfully"
                             })
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)

class StageActionViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Configuration to be modified.
    """
    queryset = StageAction.objects.all()
    serializer_class = StageActionSerializer       
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

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
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
                    if row_data[0] == 'category' or row_data[0] == 'configuration':
                        pass
                    else:
                        conf = Configuration.objects.filter(category=row_data[0],configuration=row_data[1])
                        if conf:
                            pass
                        else:
                            if row_data[2] == 'color':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_color=row_data[3], default_color=row_data[3])
                                count += 1
                            if row_data[2] == 'char':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_char=row_data[3], default_char=row_data[3])
                                count += 1
                            if row_data[2] == 'integer':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_integer=row_data[3], default_integer=row_data[3])
                                count += 1
                            if row_data[2] == 'boolean':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_boolean=row_data[3], default_boolean=row_data[3])
                                count += 1
                            if row_data[2] == 'decimal':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_decimal=row_data[3], default_decimal=row_data[3])
                                count += 1
            return Response({'status':'success', 'code':status.HTTP_200_OK,
                            'inserted':f'{count} records are inserted'
                            })
        except Exception as e:
            return Response({
                            'error_msg':str(e),
                            'status':status.HTTP_400_BAD_REQUEST
                            })
        

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
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
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
                    if row_data[0] == 'form':
                        pass
                    else:
                        try:
                            form_rec = Form.objects.get(form=row_data[0])
                        except Exception as e:
                            print('ERROR: ', str(e))
                            defective_data.append(row_data[0])
                            pass
                        else:
                            if form_rec:
                                choice_rec = Choice.objects.filter(form_id=form_rec.id, selector=row_data[1], choice=row_data[2])
                                if choice_rec:
                                    pass
                                else:
                                    Choice.objects.create(form_id=form_rec.id, selector=row_data[1],
                                                        choice=row_data[2], sequence=row_data[3],
                                                        created_by_id=request.user.id,default=row_data[4])
                                    count += 1
                            
            return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'failed':f'form matching query for {defective_data} does not exist',
                            'inserted':f'{count} records are inserted'
                            })
        except Exception as e:
            return Response({
                            'error_msg':str(e),
                            'status':status.HTTP_400_BAD_REQUEST
                            })
    
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
    
    def list(self, request, *args, **kwargs):
        queryset = Form.objects.filter().all()
        serializers = FormSerializer(queryset, many = True, context = {"request": request})
        return super().list(request, *args, **kwargs)

    
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
            # 'form__title':['exact', 'contains'],
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
    def get_columns(self, request, pk=None): 
        queryset = Column.objects.filter(list = pk) 
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
                            form_instance = Form.objects.get(form = form_data)
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
    queryset = Column.objects.all()
    serializer_class = ColumnsSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("app__name",)
    filterset_fields = {
            'position': ['exact'],'default': ['exact'],
            'required': ['exact'],'optional': ['exact'],
        }
    ordering_fields = ("__all__")
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('data')
            user_id = str(request.user.id)
            apps = []
            lists = []
            count = 0
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    if row_data[0].lower() == 'column':
                        pass
                    else:
                        try:
                            apprec = App.objects.get(name=row_data[1].lower())
                            print(apprec)
                        except Exception as e:
                            apps.append(row_data[1])
                            pass
                        else:
                            if apprec:
                                try:
                                    listrec = List.objects.get(name=row_data[2].lower())
                                except Exception as e:
                                    lists.append(row_data[2])
                                    pass
                                else:
                                    if listrec:
                                        columnrec = Column.objects.filter(column=row_data[0],app_id=apprec.id,list_id=listrec.id)
                                        if columnrec:
                                            pass
                                        else:
                                            Column.objects.create(column=row_data[0],app_id=apprec.id,list_id=listrec.id,default=row_data[3],
                                                                position=row_data[4],required=row_data[5],optional=row_data[6],created_by_id=user_id)
                                            count += 1
                            
            return Response({'invalid_app':f'{apps} are invalid app names',
                            'invalid_list':f'{lists} are invalid list names',
                            'inserted_rec':f'{count} records are inserted',
                            'status':status.HTTP_200_OK
                            })
        except Exception as e:
            return Response({
                            'error_msg':str(e),
                            'status':status.HTTP_400_BAD_REQUEST
                            })
         
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
    
    
    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.filter().all()
        serializers = MenuSerializer(queryset, many = True, context = {"request": request})
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            defective_data = []
            count = 0
            check = None
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    if row_data[0].lower() == 'category':
                        pass
                    else:
                        data_dict = {}
                        try:
                            listrec = List.objects.get(list = row_data[1])
                            data_dict['list'] = listrec.id
                        except Exception as e:
                            defective_data.append([row_data[1]])
                            continue
                        else:
                            label = row_data[2]
                            language = get_current_user_language(request.user)
                            check=Translation.objects.get(label=label, language_id=language.id)
                        if check:
                            label_rec = check
                            pass
                        else:
                            label_rec = Translation.objects.create(label=label, language_id=language.id)
                        menu_rec = Menu.objects.filter(menu_category=row_data[0], list_id = listrec.id, sequence = row_data[3])
                        if menu_rec:
                            pass
                        else:
                            if listrec:
                                data_dict['sequence'] = row_data[3]
                                data_dict['menu_category'] = row_data[0]
                            menu_serializer = MenuSerializer(data=data_dict, context={'request': request})
                            if menu_serializer.is_valid():
                                menu_serializer.save()
                                count = count + 1
                                new_trans = TranslationMenu.objects.create(menu_id=menu_serializer.data.get('id'), translation_id=label_rec.id)
            if defective_data:
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(count)+" row(s) inserted successfully",
                             'failed':f'list matching query for {defective_data} does not exist'})
            else: 
                return Response({'status':'success', 'code':status.HTTP_200_OK,
                             'inserted': str(count)+" row(s) inserted successfully"
                             })
        except Exception as e:
            response = {'status': 'error','code': status.HTTP_400_BAD_REQUEST,'message': str(e)}
            return Response(response)
    
     
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
    
       
    