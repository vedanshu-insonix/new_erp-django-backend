
from django.core.management.base import BaseCommand
from system.models.common import BaseContent
from warehouse.models import ContainerTypes
from system.models import Choice, Selectors, Currency,Country,State,Configuration,Language,Icons,List,Table,Data,Entity,Category,Menu,Column,Form,FormIcon,Stage,Entity,FormList,ListIcon
import pandas as pd
import os
from django.db import models
from django.contrib.auth.models import User
from rest_framework.response import Response
from system.views import utils



folder = r'/home/prity/Downloads/'
files = os.listdir(folder)
data_dict={}



def  extract_data(file):
    file_path = f'{folder}{file}'
    data = pd.read_excel(file_path).to_dict()
    return data

def create_selector(data):
    try:
        id = data.get("Selector ID")
        selector = data.get("System Name")
        type = data.get("Type")
        description = data.get("System Description")
        sList = list(selector.keys())
        for x in sList:
            sel_id = id.get(x)
            sName = selector.get(x)
            tp = type.get(x)
            desc = description.get(x)
            sel_rec = Selectors.objects.filter(id = sel_id,selector = sName)
            if not sel_rec:
                Selectors.objects.create(
                    id = sel_id,
                    selector = sName,
                    type = tp,
                    description = desc
                )
    except Exception as e:
        print(e)
        
def create_choice(data):
    try:
        selector = data.get('Selector')
        sel_id = data.get("Selector ID")
        choice_name = data.get('System Name')
        id = data.get("Choice ID")
        seq = data.get("Sequence")
        description = data.get("System Description")
        #default = data.get("Default")
        sList = list(selector.keys())
        for x in sList:
            choice_id = id.get(x)
            nName = choice_name.get(x)
            sel = selector.get(x)
            sequence = int(seq.get(x))
            desc = description.get(x)
            sSel = Selectors.objects.filter(selector=sel).first()
            choice_rec = Choice.objects.filter(choice_name=nName,id = choice_id)
            if not choice_rec:
                Choice.objects.create(
                        id = choice_id,
                        selector=sSel,
                        choice_name=nName,
                        sequence=sequence,
                        description = desc
                    )
    except Exception as e:
        print(e)
        
def create_dataset(data):
    try:
        id = data.get("Dataset ID")
        table = data.get('System Name')
        description = data.get('System Description')
        dList = list(table.keys())
        for x in dList:
            tbl_id = id.get(x)
            dName = table.get(x)
            desc = description.get(x)
            dataset_rec = Table.objects.filter(id= tbl_id,table=dName)
            if not dataset_rec:
                Table.objects.create(
                        id= tbl_id,
                        table=dName,
                        description=desc
                    )
    except Exception as e:
        print(e)
        
def create_data(data):
    try:
        id = data.get("Data ID")
        d_id = data.get("Dataset ID")
        dataset = data.get('Dataset')
        name = data.get('Data System Name')
        data_type =data.get('Data Type')
        description = data.get('System Description')
        field = data.get('Field')
        field_type = data.get('Field Type')
        comment= data.get('Comment')
        dList = list(name.keys())
        for x in dList:
            data_id = id.get(x)
            dName = name.get(x)
            desc = description.get(x)
            dset=dataset.get(x)
            dtype=data_type.get(x)
            f = field.get(x)
            ftype = field_type.get(x)
            cmnt = comment.get(x)
            sdset = Table.objects.get(table=dset)
            data_rec = Data.objects.filter(id = data_id,name=dName)
            if not data_rec:
                Data.objects.create(
                        id = data_id,
                        name=dName,
                        description=desc,
                        dataset=sdset,
                        data_type=dtype,
                        field= f,
                        field_type=ftype,
                        comment=cmnt
                    )
    except Exception as e:
        print(e)
        
def create_icons(data):
    try:
        id = data.get("Icon ID")
        system_name = data.get('System Name')
        icon_image = data.get('Image File')
        iList = list(system_name.keys())
        for x in iList:
            icon_id = id.get(x)
            sName = system_name.get(x)
            iImage = icon_image.get(x)
            icon_rec = Icons.objects.filter(id =icon_id,system_name=sName)
            if not icon_rec:
                Icons.objects.create(
                        id =icon_id,
                        system_name=sName,
                        icon_image=iImage,
                )
    except Exception as e:
        print(e)
        
        
def create_conf(data):
    try:
        id = data.get("Configuration ID")
        configuration = data.get('System Name')
        type = data.get('Type')
        default_value = data.get("Default Color")
        #editable = data.get("Editable")
        confList = list(configuration.keys())
        for x in confList:
            conf_id = id.get(x)
            conf = configuration.get(x)
            tp = type.get(x)
            #edit = editable.get(x)
            # if edit == 'yes' or 'Yes':
            #     edit = True
            # else:
            #     edit = False
            vdef = default_value.get(x)
            conf_rec = Configuration.objects.filter(id = conf_id,configuration=conf)
            if  not conf_rec:
                Configuration.objects.create(
                        id = conf_id,
                        configuration=conf,
                        type = tp,
                        default_value =vdef,
                       # editable = edit
                    )
    except Exception as e:
        print(e)
        
        
def create_currencies(data):
    try:
        id = data.get("Currency ID")
        name = data.get('System Name')
        code = data.get('Code')
        sym = data.get("Symbol")
        
        sList = list(name.keys())
        for x in sList:
            cur_id = id.get(x)
            xName = name.get(x)
            xCode = code.get(x)
            xSym = sym.get(x)
            cur_rec = Currency.objects.filter(id = cur_id,name=xName)
            if not cur_rec:
                Currency.objects.create(
                        id = cur_id,
                        name=xName,
                        code=xCode,
                        symbol=xSym
                    )
    except Exception as e:
        print(e)
        
def create_countries(data):
    try:
        id = data.get("Country ID")
        native_name = data.get('Native Name')
        country = data.get('System Name')
        telephone_code = data.get("Telephone Code")
        currency = data.get('Currency Name')
        cur_code = data.get("Currency Code")
        cur_id = data.get("Currency ID")
        symbol_position = data.get("Currency Symbol","")
        money_format = data.get('Money Format',"")
        date_format = data.get("Date Format","")
        time_format = data.get("Time Format","")
        conList = list(country.keys())
        for x in conList:
            con_id = id.get(x)
            cu_code =cur_code.get(x)
            cu_id = cur_id.get(x)
            nName = native_name.get(x)
            cCon=country.get(x)
            xtel= telephone_code.get(x)
            xCurr = currency.get(x)
            sym = symbol_position.get(x)
            Mon= money_format.get(x)
            Date = date_format.get(x)
            Time = time_format.get(x)
            sCur = Currency.objects.filter(code=cu_code,name =xCurr).first()
            sSym = Choice.objects.filter(choice_name=sym).first()
            sMon = Choice.objects.filter(choice_name=Mon).first()
            sDate = Choice.objects.filter(choice_name=Date).first()
            sTime = Choice.objects.filter(choice_name=Time).first()
            con_rec = Country.objects.filter(id = con_id,country = cCon)
            if not con_rec:
                Country.objects.create(
                        id = con_id,
                        native_name=nName,
                        telephone_code=xtel,
                        country = cCon,
                        currency=sCur,
                        symbol_position=sSym,
                        money_format=sMon,
                        date_format=sDate,
                        time_format = sTime
                    )
    except Exception as e:
        print(e)
        
def create_state(data):
    try:
        id = data.get("State ID")
        country = data.get('Country Name')
        con_code = data.get("Country Code")
        con_id = data.get("Country ID")
        name = data.get('System Name')
        seq = data.get("Sequence")
        sList = list(name.keys())
        for x in sList:
            s_id = id.get(x)
            c_code = con_code.get(x)
            c_id = con_id.get(x)
            con = country.get(x)
            sCon = Country.objects.filter(country=con).first()
            sequence = int(seq.get(x))
            state_rec = State.objects.filter(id = s_id,name= name)
            if not state_rec:
                State.objects.create(
                        id = s_id,
                        country=sCon,
                        name=name.get(x),
                        sequence = sequence
                    )
    except Exception as e:
        print(e)
        
def create_language(data):
    try:
        id = data.get("Language ID")
        name = data.get('System Name')
        native_Translation = data.get('Native Name')
        code = data.get("Code")
        direction = data.get("Direction")
        dir_choice = data.get("Direction Choice ID")
        langList = list(native_Translation.keys())
        for x in langList:
            l_id =  id.get(x)
            xName = name.get(x)
            dir_c = dir_choice.get(x)
            nTrans = native_Translation.get(x)
            cod = code.get(x)
            dir = direction.get(x)
            sChoice = Choice.objects.filter(choice_name=dir).first()
            lang_rec =Language.objects.filter(id =l_id,name=xName)
            if not lang_rec:
                Language.objects.create(
                        id =l_id,
                        name=xName,
                        native_Translation = nTrans,
                        code = cod,
                        direction = sChoice
                        
                    )
    except Exception as e:
        print(e)
        
def create_list(data):
    try:
        id = data.get("List ID")
        system_name = data.get('System Name')
        category = data.get('Category')
        primary_table = data.get("Dataset")
        description = data.get("System Description")
        #label = data.get('Translation - US English')
        list_type = data.get('List Type')
        default_view = data.get("Default View")
        icon = data.get("Icon System Name")
        icon_id = data.get("Icon ID")
        primary = data.get("Primary Form")
        type_id = data.get("Type Choice ID")
        lList = list(system_name.keys())
        for x in lList:
            l_id = id.get(x)
            desc = description.get(x)
            def_view = default_view.get(x)
            i_name = icon.get(x)
            i_id = icon_id.get(x)
            p_form = primary.get(x)
            lName = system_name.get(x)
            ptable = primary_table.get(x)
            cat = category.get(x)
            t_id = type_id.get(x)
            ltype = list_type.get(x)
            gicon = Icons.objects.filter(system_name=i_name,id = i_id).first()
            gccat= Choice.objects.get_or_create(choice_name= cat)
            sptble = Table.objects.filter(table=ptable).first()
            #sltp = Choice.objects.filter(choice_name=ltype,id = t_id).first()
            list_rec = List.objects.filter(system_name=lName)
            if not list_rec:
                List.objects.create(
                        id = l_id,
                        system_name=lName,
                        primary_table=sptble,
                        #list_type =sltp,
                        description = desc,
                        #label = lbl,
                        default_view = def_view,
                        
                    )
                # form_rec= FormList.objects.filter( list_id = l_id,primary = p_form)
                # if not form_rec:
                #     FormList.objects.create(
                #         list_id = l_id,
                #         primary = p_form
                #     )
                lIcon_rec = ListIcon.objects.filter(list_id = l_id,icon =gicon)
                if  not lIcon_rec:
                    ListIcon.objects.create(
                        list_id = l_id,
                        icon =gicon
                    )
                
    except Exception as e:
        print(e)
        
def create_menu(data):
    try:
        id = data.get("Menu Item ID")
        name = data.get("System Name")
        category_choice = data.get('Category')
        #description = data.get("System Description")
        seq = data.get('Sequence')
        lists = data.get('List')
        listID = data.get("List ID")
        visibility = data.get('Visibility')
        lList = list(name.keys())
        for x in lList:
            menu_id= id.get(x)
            mName = name.get(x)
            cCat =category_choice.get(x)
            #desc=description.get(x)
            list_name = lists.get(x)
            sequence = int(seq.get(x))
            vis = visibility.get(x)
            lst = listID.get(x)
            sclist= List.objects.filter(id= lst ,system_name=list_name).first()
            #svis = Choice.objects.filter(choice_name=vis).first()
            sCat = Choice.objects.filter(choice_name=cCat).first()
            menu_rec = Menu.objects.filter( id = menu_id,name=mName)
            if not menu_rec:
                Menu.objects.create(
                            id = menu_id,
                            list= sclist,
                            name=mName,
                            category_choice=sCat,
                            #visibility=svis,
                            # description= desc,
                            sequence = sequence
                        )
    except Exception as e:
        print(e)
        
    
def create_columns(data):
    try:
        id = data.get("Column ID")
        clist = data.get('List')
        l_id = data.get("List ID")
        column = data.get('System Name')
        seq = data.get("Sequence")
        dataset=data.get('Dataset')
        d_id =data.get("Dataset ID")
        visibility = data.get('Visibility')
        data_id = data.get("Data ID")
        data = data.get('Data System Name')
        sList = list(clist.keys())
        for x in sList:
            col_id =id .get(x) 
            tbl_id = d_id.get(x)
            dt_id =data_id.get(x)
            cl = clist.get(x)
            col = column.get(x)
            dts = dataset.get(x)
            vsb= visibility.get(x)
            dt = data.get(x)
            gclist = List.objects.filter(system_name=cl).first()
            gcvsb = Choice.objects.filter(choice_name=vsb).first()
            gctble = Table .objects.filter(table=dts).first()
            gcdata = Data.objects.filter(name=dt).first()
            col_rec= Column.objects.filter(id = col_id,column = col)
            if not col_rec:
                Column.objects.create(
                    id = col_id,
                    clist = gclist,
                    column = col,
                    dataset = gctble,
                    data = gcdata,
                    visibility = gcvsb
                )
    except Exception as e:
        print(e)
        
        
def create_forms(data):
    try:
        form = data.get('System Name')
        description=data.get("System Description")
        icon = data.get("Icon")
        id = data.get("Form ID")
        icon_id = data.get("Icon ID")
        fList = list(form.keys())
        for x in fList:
            nName = form.get(x)
            desc = description.get(x)
            formId = id.get(x)
            ic_id = icon_id.get(x)
            icn= icon.get(x)
            form_icon = Form.objects.filter(form=nName).first()
            form_rec = Form.objects.filter(form=nName,id = formId)
            if len(form_rec) < 1:
                Form.objects.create(
                        id = formId,
                        form=nName,
                        description = desc,
                    )
            # if id is not None and icon is not None:
            gform = Icons.objects.filter(system_name = icn).first()
            formIcon_rec= FormIcon.objects.filter(form =form_icon,icon=gform)
            if len(formIcon_rec) < 1:
                FormIcon.objects.create(
                    icon_id=ic_id,
                    form =form_icon,
                    icon=gform
                )
    except Exception as e:
        print(e)
        

def create_entities(data):
    try:
        id = data.get("Entity ID")
        name = data.get("System Name")
        parent = data.get("Parent Name")
        parent_id = data.get("Parent ID")
        eList = list(name.keys())
        for x in eList:
            ent_id = id.get(x)
            eName = name.get(x)
            prnt = parent.get(x)
            prnt_id = parent_id.get(x)
            gcprnt = Entity.objects.filter(name=prnt).first()
            entity_rec = Entity.objects.filter(name = eName,id = ent_id)
            if len(entity_rec) < 1:
                Entity.objects.create(
                    id = ent_id,
                    name = eName,
                    parent = gcprnt
                )
    except Exception as e:
        print(e)


def create_container(data):
    try:
        id = data.get("Container ID")
        container = data.get("System Name")
        dimension_1 = data.get("Dimension 1")
        dimension_2 = data .get("Dimension 2")
        dimension_3 = data.get("Dimension 3")
        weight = data.get("Weight")
        surcharge = data .get("Surcharge")
        description = data .get("System Description")
        #stage = data.get("")
        #status_choice_id = data.get("")
        cList = list(container.keys())
        for x in cList:
            cont_id = id.get(x)
            cont= container.get(x)
            dim_1 = dimension_1.get(x)
            dim_2 = dimension_2.get(x)
            dim_3 = dimension_3.get(x)
            wt = weight.get(x)
            sch =  surcharge.get(x)
            desc = description.get(x)
            #print(type(sch))
           
            cont_rec = ContainerTypes.objects.filter(container = cont)
            if not cont_rec:
                ContainerTypes.objects.create(
                    id = cont_id,
                    container = cont,
                    dimension_1 = dim_1,
                    dimension_2 = dim_2,
                    dimension_3 = dim_3,
                    weight = wt,
                    #surcharge = sch,
                    description = desc
                )
            
            
    except Exception as e:
        print(e)
        
class Command(BaseCommand):
    help = "load data from import api's "
    
    def handle(self, *args, **kwargs):
        for file in files:
            if file.endswith('.xlsx'):
                data = extract_data(file)
                
                if file == "SelectorsFeb12.xlsx":
                    result = create_selector(data)
                if file == "ChoicesFeb14.xlsx":
                    result = create_choice(data)
                                    
                if file == "DatasetsFeb12.xlsx":
                    result = create_dataset(data)
                        
                if file == "DataFeb14.xlsx":
                    result = create_data(data)
                        
                if file == "IconsFeb13.xlsx":
                    result = create_icons(data)
                        
                if file == "ConfigurationsFeb12.xlsx":
                    result = create_conf(data) 
                               
                if file == "CurrenciesFeb12.xlsx":
                    result = create_currencies(data)
                      
                if file == "CountriesFeb12.xlsx":
                    result = create_countries(data)
                        
                if file == "StatesFeb12.xlsx":
                    result= create_state(data)
                    
                if file == "LanguagesFeb12.xlsx":
                    result = create_language(data)
                        
                if file == "ListsFeb12.xlsx":
                    result = create_list(data)
               
                        
                if file == "MenuItemsFeb12.xlsx":
                    result = create_menu(data)
     
                if file == "ColumnsFeb12.xlsx":
                    result = create_columns(data)
                    
                if file == "FormsFeb12.xlsx":
                    result = create_forms(data)
                    
                # if file == "new_Stage.xlsx":
                #     result = create_Stages(data)
                
                if file == "EntitiesFeb14.xlsx":
                    result = create_entities(data)
                
                
                if file == "ContainerTypesFeb14.xlsx":
                    result = create_container(data)