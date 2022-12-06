from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializers import *
from ..models.columns import Column
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from system import utils
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
    
    def list(self, request, args, *kwargs):
        queryset = Stage.objects.filter().all()
        serializers = StageSerializer(queryset, many = True, context = {"request": request})
        return super().list(request, args, *kwargs)
    

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                data_dict = {}
                defective_data=[]
                count=0
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    stage_name=row_data[2]
                    if stage_name:
                        if row_data[0] == 'form' or row_data[0] == 'Form':
                            pass
                        else:
                            form_name=row_data[0]
                            form_rec = Form.objects.filter(form=form_name)
                            if form_rec:
                                stage_rec = Stage.objects.filter(stage = stage_name,form_id=form_rec.values()[0]['id'])
                                if stage_rec:
                                    pass
                                else:
                                    data_dict['form']=form_rec.values()[0]['id']
                                    data_dict['sequence']=row_data[1]
                                    data_dict['stage']=stage_name
                                    data_dict['created_by_id']=user_id
                                    serializer=StageSerializer(data=data_dict,context={'request': request})
                                    if serializer.is_valid():
                                        serializer.save()
                                        count += 1
                                        stage_rec = Stage.objects.filter(stage = stage_name,form_id=form_rec.values()[0]['id'])
                                req_action = row_data[3]
                                opt_action = row_data[4]
                                if req_action:
                                    text_split = req_action.split(',')
                                    for i in range (len(text_split)):
                                        check = StageAction.objects.filter(stage_id=stage_rec.values()[0]['id'],action=text_split[i])
                                        if check:
                                            pass
                                        else:
                                            StageAction.objects.create(stage_id=stage_rec.values()[0]['id'],action=text_split[i],required=True)
                                if opt_action:
                                    text_split = opt_action.split(',')
                                    for i in range (len(text_split)):
                                        check = StageAction.objects.filter(stage_id=stage_rec.values()[0]['id'],action=text_split[i])
                                        if check:
                                            pass
                                        else:
                                            StageAction.objects.create(stage_id=stage_rec.values()[0]['id'],action=text_split[i],optional=True)
                            else:
                                defective_data.append(row_data[0])
                if defective_data:
                    defective_data = {
                        "missing_form" : f"These {set(defective_data)} are the invalid form names."
                    }
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

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
            count = 0
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    data_dict={}
                    conf_name=row_data[1]
                    if conf_name:
                        if row_data[0] == 'category' or row_data[0] == 'Category':
                            pass
                        else:
                            conf = Configuration.objects.filter(category=row_data[0],configuration=row_data[1])
                            if conf:
                                pass
                            else:
                                data_dict['category']=row_data[0]
                                data_dict['configuration']=row_data[1]
                                data_dict['type']=row_data[2]
                                data_dict['current_value']=row_data[3]
                                data_dict['default_value']=row_data[3]
                                serializer=ConfigurationSerializer(data=data_dict,context={'request': request})
                                if serializer.is_valid():
                                    serializer.save()
                                    count += 1
                return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
            
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
            data_dict = {}
            count = 0
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    choice_name=row_data[1]
                    label=row_data[4]
                    if choice_name:
                        if row_data[0] == 'selector' or row_data[0]=='Selector':
                            pass
                        else:
                            language = get_current_user_language(request.user)
                            lang = Language.objects.filter(name=language)
                            check=Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                            if check:
                                pass
                            else:
                                new_label = Translation.objects.create(label=label,language_id=lang.values()[0]['id'])
                            label_rec = Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                            
                            choice_rec = Choice.objects.filter(selector=row_data[0], choice=choice_name)
                            if choice_rec:
                                choice_id=choice_rec.values()[0]['id']
                                pass
                            else:
                                data_dict['selector']=row_data[0]
                                data_dict['choice']=row_data[1]
                                data_dict['sequence']=row_data[2]
                                data_dict['created_by_id']=user_id
                                
                                if row_data[3]:
                                    data_dict['default']=row_data[3]
                                else:
                                    data_dict['default']=False
                                serializer=ChoiceSerializer(data=data_dict,context={'request': request})
                                if serializer.is_valid(raise_exception=True):
                                    serializer.save()
                                    count += 1
                                    choice_id= serializer.data.get('id')
                            trans = TranslationChoice.objects.filter(choice_id=choice_id, translation_id=label_rec.values()[0]['id'])
                            if trans:
                                pass
                            else:
                                TranslationChoice.objects.create(choice_id=choice_id, translation_id=label_rec.values()[0]['id']) 
                return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

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
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            count = 0
            data_dict = {}
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)
                    form_name=row_data[0]
                    if form_name:
                        if row_data[0].lower() == 'form':
                            pass
                        else:
                            form_rec = Form.objects.filter(form=form_name)
                            if form_rec:
                                pass
                            else:
                                data_dict['form'] = row_data[0]
                                data_dict['created_by_id'] = user_id
                                serializer=FormSerializer(data=data_dict,context={'request': request})
                                if serializer.is_valid():
                                    serializer.save()
                                    count += 1
                return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))

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
        serializer = ColumnsSerializer(queryset, many = True, context={'request': request})         
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            user_id = str(request.user.id)
            if file:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                defective_data = []
                count = 0
                for row in sheet.iter_rows():
                    row_data = []
                    for cell in row:
                        row_data.append(cell.value)

                    category=row_data[0]
                    list_data = row_data[1]
                    data_source = row_data[2]
                    label=row_data[3]
                    sequence_data = row_data[4]
                    description = row_data[5]
                    data_filter = row_data[6]
                    data_sort = row_data[7]

                    if list_data:
                        if row_data[0] == 'category' or row_data[0] == 'Category':
                            pass
                        else:
                            data_dict = {}
                            data_source=row_data[2]
                            data_dict['data_source'] = data_source
                            data_dict['created_by_id']=user_id
                            if list_data:
                                list_data = list_data
                                data_dict['list'] = list_data
                            if sequence_data:
                                data_dict['sequence'] = sequence_data
                            if data_filter:
                                data_dict['data_filter'] = data_filter
                            if data_sort:
                                data_dict['data_sort'] = data_sort
                            if description:
                                data_dict['description'] = description
                            list_name=data_dict['list']
                            list_rec = List.objects.filter(list=list_name)
                            if list_rec:
                                list_id=list_rec.values()[0]['id']
                                pass
                            else:
                                list_serializers = ListSerializer(data=data_dict, context={'request': request})
                                if list_serializers.is_valid(raise_exception=True):
                                    list_serializers.save()
                                    count = count + 1
                                    
                                list_id=list_serializers.data.get('id')

                            language = get_current_user_language(request.user)
                            lang = Language.objects.filter(name=language)
                            if label:
                                check=Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                                if check:
                                    pass
                                else:
                                    new_label = Translation.objects.create(label=label,language_id=lang.values()[0]['id'])
                                label_rec = Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                                trans = TranslationList.objects.filter(list_id=list_id, translation_id=label_rec.values()[0]['id'])
                                if trans:
                                    pass
                                else:
                                    TranslationList.objects.create(list_id=list_id, translation_id=label_rec.values()[0]['id'])

                            if category:
                                menu_rec = Menu.objects.filter(menu_category=category,list_id=list_id)
                                if menu_rec:
                                    pass
                                else:
                                    mdict = {}
                                    mdict['menu_category']=category
                                    mdict['list']=list_id
                                    mrec=MenuSerializer(data=mdict, context={'request': request})
                                    if mrec.is_valid():
                                        mrec.save()
                            else:
                                defective_data.append([data_source])
                if defective_data:
                    defective_data = {
                        "missing_form" : f"These {set(defective_data)} are the invalid form names."
                    } 
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
     
class ColumnsViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows Columns to be modified.
    """
    queryset = Column.objects.all()
    serializer_class = ColumnsSerializer  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = ("app__name",)
    filterset_fields = {
            'position': ['exact'],'visibility': ['exact']
        }
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
                    column = row_data[1]
                    field = row_data[4]
                    if column and field:
                        if row_data[0] == 'list' or row_data[0] == 'List':
                            pass
                        else:
                            list  = row_data[0]
                            listrec = List.objects.filter(list=list)
                            if listrec:
                                columnrec = Column.objects.filter(column= column,list_id=listrec.values()[0]['id'])
                                if columnrec:
                                    pass
                                else:
                                    Column.objects.create(column=column,list_id=listrec.values()[0]['id'],position=row_data[3],visibility=row_data[2],created_by_id=user_id, table = row_data[4], field = row_data[5])
                                    count = count+1
                            else:
                                defective_data.append(row_data[0])
                if defective_data:
                    defective_data = {
                        "missing_lists" : f"These {defective_data} are the invalid list names."
                    } 
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
        
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
                    menu_category = row_data[0]
                    if menu_category:
                        if row_data[0].lower() == 'category':
                            pass
                        else:
                            data_dict = {}
                            list = row_data[1]
                            listrec = List.objects.filter(list=list)
                            if listrec:
                                label = row_data[2]
                                language = get_current_user_language(request.user)
                                lang = Language.objects.filter(name=language)
                                check=Translation.objects.filter(label=label, language_id=lang.values()[0]['id'])
                                if check:
                                    pass
                                else:
                                    new_label = Translation.objects.create(label=label, language_id=lang.values()[0]['id'])
                                label_rec = Translation.objects.filter(label=label, language_id=lang.values()[0]['id'])
                                menu_rec = Menu.objects.filter(menu_category=row_data[0], list_id = listrec.values()[0]['id'], sequence = row_data[3])
                                if menu_rec:
                                    pass
                                else:
                                    data_dict['list'] = listrec.values()[0]['id']
                                    data_dict['sequence'] = row_data[3]
                                    data_dict['menu_category'] = row_data[0]
                                    menu_serializer = MenuSerializer(data=data_dict, context={'request': request})
                                    if menu_serializer.is_valid():
                                        menu_serializer.save()
                                        count = count + 1
                                        new_trans = TranslationMenu.objects.create(menu_id=menu_serializer.data.get('id'), translation_id=label_rec.values()[0]['id'])
                            else:
                                defective_data.append(row_data[1])
                if defective_data:
                    defective_data = {
                        "missing_lists" : f"These {set(defective_data)} are the invalid list names."
                    } 
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            print(str(e))
            return Response(utils.error(self,str(e)))
    
     
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
                    data=row_data[1]
                    table = row_data[2]
                    print('table is',table)
                    field = row_data[3]
                    type = row_data[4]
                    parent_field = row_data[5]
                    link = row_data[6]
                    if data and field:
                        if row_data[0] == 'form' or row_data[0] == 'Form' :
                            pass
                        else:
                            formrec = Form.objects.filter(form=row_data[0])
                            if formrec:
                                columnrec = FormData.objects.filter(data= row_data[1],form_id=formrec.values()[0]['id'])
                                if columnrec:
                                    pass
                                else:
                                    FormData.objects.create(form_id=formrec.values()[0]['id'],data=data, table = table
                                                            ,field=field,created_by_id=user_id, type = type.lower(),
                                                            parent_field=parent_field, link=link)
                                    count += 1
                            else:
                                defective_data.append(row_data[0])
                if defective_data:
                    defective_data = {
                        "missing_forms" : f"These {set(defective_data)} are the invalid form names."
                    } 
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
    