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
from django.db.models import Q


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#**********************************Function To Extract Data From Excel File******************************************#
def importing_data(file):
    xl_data = []
    heading = []
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    max_col = sheet.max_column
    for i in range(1, max_col+1):
        cell_obj = sheet.cell(row = 1, column = i)
        heading.append((cell_obj.value).lower())
    for row in sheet.iter_rows(min_row=2):
        data_dict={}
        row_data = []
        for cell in row:
            row_data.append(cell.value)
        for i in range(len(row_data)):
            data_dict[heading[i]]=row_data[i]
        xl_data.append(data_dict)
    return(xl_data)

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

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                data_dict = importing_data(file)
                count = 0
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        try:
                            serializer=CurrencySerializer(data=data_dict[i], context={'request':request})
                            if serializer.is_valid(raise_exception=True):
                                serializer.save()
                                count += 1
                        except Exception as e:
                            pass          
                return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
           
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

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data=[]
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        currency=data_dict[i].get('currency')
                        if currency:
                            check = Currency.objects.filter(name=currency)
                            if check:
                                data_dict[i]['currency']=check.values()[0]['id']
                                try:
                                    serializer=CountrySerializer(data=data_dict[i], context={'request':request})
                                    if serializer.is_valid(raise_exception=True):
                                        serializer.save()
                                        count += 1
                                except Exception as e:
                                    print(str(e))
                                    pass
                            else:
                                defective_data.append(currency)
                if defective_data:
                    defective_data = {
                        "inavlid_currencies" : f"These {set(defective_data)} are the invalid currency names."
                    }
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
        
class StateViewSet(viewsets.ModelViewSet):
    """
    API’s endpoint that allows State to be modified.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("__all__")
    ordering_fields = ("__all__")

    @action(detail=False, methods=['post'], name='import_data', url_path = "import")
    def import_data(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data=[]
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        country=data_dict[i].get('country')
                        if country:
                            check = Country.objects.filter(Q(country__name=country) | Q(country=country))
                            if check:
                                data_dict[i]['country']=check.values()[0]['id']
                                state_name = data_dict[i].get('name')
                                state_check=State.objects.filter(name=state_name, country=data_dict[i]['country'])
                                if state_check:
                                    pass
                                else:
                                    try:
                                        serializer=StateSerializer(data=data_dict[i], context={'request':request})
                                        if serializer.is_valid(raise_exception=True):
                                            serializer.save()
                                            count += 1
                                    except Exception as e:
                                        print(str(e))
                                        pass
                            else:
                                defective_data.append(country)
                if defective_data:
                    defective_data = {
                        "inavlid_country" : f"These {set(defective_data)} are the invalid country names."
                    }
                    return Response(utils.success_def(self,count,defective_data))
                else:
                    return Response(utils.success(self,count))
            else:
                msg="Please Upload A Suitable Excel File."
                return Response(utils.error(self,msg))
        except Exception as e:
            return Response(utils.error(self,str(e)))
    
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
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data=[]
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        stage_name = data_dict[i]['stage']
                        if stage_name:
                            form_name = data_dict[i]['form']
                            form_rec = Form.objects.filter(form=form_name)
                            if form_rec:
                                req_action = data_dict[i].pop('required action buttons')
                                opt_action = data_dict[i].pop('optional action buttons')
                                data_dict[i]['form']=form_rec.values()[0]['id']
                                stage_rec = Stage.objects.filter(stage = stage_name,form_id=form_rec.values()[0]['id'])
                                if stage_rec:
                                    stage_id = stage_rec.values()[0]['id']
                                else:
                                    serializer=StageSerializer(data=data_dict[i],context={'request': request})
                                    if serializer.is_valid():
                                        serializer.save()
                                        count += 1
                                    stage_rec = Stage.objects.get(stage = stage_name,form_id=form_rec.values()[0]['id'])
                                    stage_id=stage_rec.id
                                if req_action:
                                    text_split = req_action.split(',')
                                    for i in range (len(text_split)):
                                        check = StageAction.objects.filter(stage_id=stage_id,action=text_split[i])
                                        if check:
                                            pass
                                        else:
                                            StageAction.objects.create(stage_id=stage_id,action=text_split[i],required=True)
                                if opt_action:
                                    text_split = opt_action.split(',')
                                    for i in range (len(text_split)):
                                        check = StageAction.objects.filter(stage_id=stage_id,action=text_split[i])
                                        if check:
                                            pass
                                        else:
                                            StageAction.objects.create(stage_id=stage_id,action=text_split[i],optional=True)
                            else:
                                defective_data.append(form_name)
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
            if file:
                data_dict = importing_data(file)
                count = 0
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        conf_name = data_dict[i]['configuration']
                        if conf_name:
                            category = data_dict[i]['category']
                            conf = Configuration.objects.filter(category=category,configuration=conf_name)
                            if conf:
                                pass
                            else:
                                serializer=ConfigurationSerializer(data=data_dict[i],context={'request': request})
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
            if file:
                data_dict = importing_data(file)
                count = 0
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        choice_name=data_dict[i]['choice']
                        label=data_dict[i].pop('label (us english)')
                        selector=utils.encode_api_name(data_dict[i]['selector'])
                        default=data_dict[i]['default']
                        if choice_name:
                            language = get_current_user_language(request.user)
                            lang = Language.objects.filter(name=language)
                            check=Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                            if check:
                                pass
                            else:
                                new_label = Translation.objects.create(label=label,language_id=lang.values()[0]['id'])
                            label_rec = Translation.objects.filter(label=label,language_id=lang.values()[0]['id'])
                            
                            choice_rec = Choice.objects.filter(selector=selector, choice=choice_name)
                            if choice_rec:
                                choice_id=choice_rec.values()[0]['id']
                                pass
                            else:
                                if default:
                                    continue
                                else:
                                    data_dict[i]['default']=False
                                serializer=ChoiceSerializer(data=data_dict[i],context={'request': request})
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
            print(file)
            if file:
                data_dict = importing_data(file)
                count = 0
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        form_name = data_dict[i]['form']
                        form_rec = Form.objects.filter(form=form_name)
                        if form_rec:
                            pass
                        else:
                            serializer=FormSerializer(data=data_dict[i],context={'request': request})
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
                    #data_filter = row_data[6]
                    #data_sort = row_data[7]

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
                            """if data_filter:
                                data_dict['data_filter'] = data_filter
                            if data_sort:
                                data_dict['data_sort'] = data_sort"""
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
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data=[]
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        column = data_dict[i]['column']
                        field = data_dict[i]['field']
                        if column and field:
                            list = data_dict[i]['list']
                            listrec = List.objects.filter(list=list)
                            if listrec:
                                data_dict[i]['list'] = listrec.values()[0]['id']
                                columnrec = Column.objects.filter(column= column,list_id=listrec.values()[0]['id'])
                                if columnrec:
                                    pass
                                else:
                                    serializer = ColumnsSerializer(data=data_dict[i],context={'request': request})
                                    if serializer.is_valid(raise_exception=True):
                                        serializer.save()
                                        count = count+1
                            else:
                                defective_data.append(list)
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
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data = []
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        menu_category = data_dict[i]['menu_category']
                        if menu_category:
                            list = data_dict[i]['list']
                            sequence = data_dict[i]['sequence']
                            if list:
                                listrec = List.objects.filter(list=list)
                                if listrec:
                                    data_dict[i]['list'] = listrec.values()[0]['id']
                                    list_id = listrec.values()[0]['id']
                                    menu_rec = Menu.objects.filter(menu_category=menu_category, list_id = list_id, sequence = sequence)
                                else:
                                    defective_data.append(list)
                            else:
                                data_dict[i]['list'] = None
                                menu_rec = Menu.objects.filter(menu_category=menu_category)
                            label = data_dict[i].pop('label (us english)')
                            language = get_current_user_language(request.user)
                            lang = Language.objects.filter(name=language)
                            check=Translation.objects.filter(label=label, language_id=lang.values()[0]['id'])
                            if check:
                                pass
                            else:
                                new_label = Translation.objects.create(label=label, language_id=lang.values()[0]['id'])
                            label_rec = Translation.objects.filter(label=label, language_id=lang.values()[0]['id'])
                            if menu_rec:
                                pass
                            else:
                                menu_serializer = MenuSerializer(data=data_dict[i], context={'request': request})
                                if menu_serializer.is_valid(raise_exception=True):
                                    menu_serializer.save()
                                    count = count + 1
                                    new_trans = TranslationMenu.objects.create(menu_id=menu_serializer.data.get('id'), translation_id=label_rec.values()[0]['id'])
                if defective_data:
                    defective_data = {
                        "invalid_lists" : f"These {set(defective_data)} are the invalid list name(s)."
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
            if file:
                data_dict = importing_data(file)
                count = 0
                defective_data=[]
                for i in range(len(data_dict)):
                    if data_dict[i] != None:
                        data=data_dict[i]['data']
                        field = data_dict[i]['field']
                        if data and field:
                            form_name=data_dict[i]['form']
                            formrec = Form.objects.filter(form=form_name)
                            if formrec:
                                columnrec = FormData.objects.filter(data=data,form_id=formrec.values()[0]['id'])
                                if columnrec:
                                    pass
                                else:
                                    data_dict[i]['form']=formrec.values()[0]['id']
                                    data_dict[i]['type']=(data_dict[i]['type']).lower()
                                    serializer=FormDataSerializer(data=data_dict[i], context={'request':request})
                                    if serializer.is_valid(raise_exception=True):
                                        serializer.save()
                                        count += 1
                            else:
                                defective_data.append(form_name)
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