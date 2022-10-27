from ast import For
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.common_serializers import *
from ..models.columns import Column
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from system import utils
import os
import openpyxl
from ..utils import *


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
                    if row_data[0].lower() == 'form':
                        pass
                    else:
                        form_rec = Form.objects.filter(form=row_data[0])
                        if form_rec:
                            stage_rec = Stage.objects.filter(stage = row_data[2],form_id=form_rec.values()[0]['id'])
                            if stage_rec:
                                pass
                            else:
                                data_dict['form']=form_rec.values()[0]['id']
                                data_dict['sequence']=row_data[1]
                                data_dict['stage']=row_data[2]
                                data_dict['created_by_id']=user_id
                                serializer=StageSerializer(data=data_dict,context={'request': request})
                                if serializer.is_valid():
                                    serializer.save()
                                    count += 1
                                    stage_rec = Stage.objects.filter(stage = row_data[2],form_id=form_rec.values()[0]['id'])
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
                if defective_data:
                    defective_data = {
                        "missing_form" : f"These {defective_data} are the invalid form names."
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
                    if row_data[0] == 'category' or row_data[0] == 'configuration':
                        pass
                    else:
                        conf = Configuration.objects.filter(category=row_data[0],configuration=row_data[1])
                        if conf:
                            pass
                        else:
                            if row_data[2] == 'color':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_value=row_data[3], default_value=row_data[3])
                                count += 1
                            if row_data[2] == 'char':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_value=row_data[3], default_value=row_data[3])
                                count += 1
                            if row_data[2] == 'integer':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_value=row_data[3], default_value=row_data[3])
                                count += 1
                            if row_data[2] == 'boolean':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_value=row_data[3], default_value=row_data[3])
                                count += 1
                            if row_data[2] == 'decimal':
                                new_conf = Configuration.objects.create(category=row_data[0],configuration=row_data[1],type=row_data[2], current_value=row_data[3], default_value=row_data[3])
                                count += 1
                return Response(utils.success(self,count))
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
            defective_data = []
            data_dict = {}
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
                        form_rec = Form.objects.filter(form=row_data[0])
                        if form_rec:
                            choice_rec = Choice.objects.filter(form_id=form_rec.values()[0]['id'], selector=row_data[1], choice=row_data[2])
                            if choice_rec:
                                pass
                            else:
                                data_dict['form']=form_rec.values()[0]['id']
                                data_dict['selector']=row_data[1]
                                data_dict['choice']=row_data[2]
                                data_dict['sequence']=row_data[3]
                                data_dict['created_by_id']=user_id
                                if row_data[4] == 'yes':
                                    data_dict['default']=True
                                elif row_data[4] == 'no':
                                    data_dict['default']=False
                                serializer=ChoiceSerializer(data=data_dict,context={'request': request})
                                if serializer.is_valid():
                                    serializer.save()
                                    count += 1
                        else:
                            defective_data.append(row_data[0])    
                if defective_data:
                    defective_data = {
                        "missing_form" : f"These {defective_data} are the invalid form names."
                    } 
                    return Response(utils.success_def(self,count,defective_data))
                else:
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
                    if row_data[0].lower() == 'form':
                        pass
                    else:
                        formrec = Form.objects.filter(form=row_data[0].lower())
                        if formrec:
                            pass
                        else:
                            # data_dict['form'] = row_data[0].lower()
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
                    if row_data[0].lower() == 'form' or row_data[0].lower() == 'list' or row_data[0].lower() == 'sequence':
                        pass
                    else:
                        form_data = row_data[0]
                        list_data = row_data[1]
                        sequence_data = row_data[2]
                        
                        data_dict = {}
                        form_instance = Form.objects.filter(form = form_data)
                        if form_instance:
                            data_dict['form'] = form_instance.values()[0]['id']
                            data_dict['created_by_id']=user_id
                            if list_data:
                                if " " in list_data:
                                    list_data.replace(" ","_")
                                list_data = list_data.lower()
                                data_dict['list'] = list_data
                            if sequence_data:
                                data_dict['sequence'] = sequence_data
                            list_serializers = ListSerializer(data=data_dict, context={'request': request})
                            if list_serializers.is_valid():
                                list_serializers.save()
                                count = count + 1
                        else:
                            defective_data.append([form_data])
                if defective_data:
                    defective_data = {
                        "missing_form" : f"These {defective_data} are the invalid form names."
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
            'position': ['exact'],'default': ['exact'],
            'required': ['exact'],'optional': ['exact'],
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
                    if row_data[0].lower() == 'column':
                        pass
                    else:
                        listrec = List.objects.filter(list=row_data[1].lower())
                        if listrec:
                            columnrec = Column.objects.filter(column=row_data[0],list_id=listrec.values()[0]['id'])
                            if columnrec:
                                pass
                            else:
                                type=row_data[3]
                                if type=='required':
                                    Column.objects.create(column=row_data[0],list_id=listrec.values()[0]['id'],position=row_data[2],required=True,created_by_id=user_id)
                                    count += 1
                                elif type=='optional':
                                    Column.objects.create(column=row_data[0],list_id=listrec.values()[0]['id'],position=row_data[2],optional=True,created_by_id=user_id)
                                    count += 1
                                elif type=='default':
                                    Column.objects.create(column=row_data[0],list_id=listrec.values()[0]['id'],position=row_data[2],default=True,created_by_id=user_id)
                                    count += 1
                                else:
                                    pass
                        else:
                            defective_data.append(row_data[1])
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
                    if row_data[0].lower() == 'category':
                        pass
                    else:
                        data_dict = {}
                        listrec = List.objects.filter(list=row_data[1].lower())
                        if listrec:
                            label = row_data[2]
                            language = get_current_user_language(request.user)
                            check=Translation.objects.filter(label=label, language_id=language.id)
                            if check:
                                pass
                            else:
                                new_label = Translation.objects.create(label=label, language_id=language.id)
                            label_rec = Translation.objects.filter(label=label, language_id=language.id)
                            menu_rec = Menu.objects.filter(menu_category=row_data[0], list_id = listrec.values()[0]['id'], sequence = row_data[3])
                            if menu_rec:
                                pass
                            else:
                                data_dict['list'] = listrec.values()[0]['id']
                                data_dict['sequence'] = row_data[3]
                                data_dict['menu_category'] = row_data[0]
                                print(data_dict)
                                menu_serializer = MenuSerializer(data=data_dict, context={'request': request})
                                if menu_serializer.is_valid():
                                    menu_serializer.save()
                                    count = count + 1
                                    new_trans = TranslationMenu.objects.create(menu_id=menu_serializer.data.get('id'), translation_id=label_rec.values()[0]['id'])
                        else:
                            defective_data.append(row_data[1])
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
    
       
    