from django.core.management.base import BaseCommand
from warehouse.models import ContainerTypes
from system.models import Choice, RecordIdentifiers,Selectors,Currency,Country,State,Configuration,Language,Icons,List,DataTable,Data,Entity,Menu,Column,Form,FormIcon,Stage,Entity,FormList,ListIcon
import pandas as pd
import os
from system.models.translations import TranslationSelector,TranslationChoice,TranslationColumn,TranslationForm,TranslationStage,TranslationList,TranslationMenu,TranslationData,TranslationIcons,TranslationCurrency,TranslationConfiguration,TranslationContainerType,Translation
from system.service import get_rid_pkey, updatenextid
from django.contrib.auth.models import User

folder = r'./managementCommandsFiles/'
files = os.listdir(folder)
data_dict={}
global_data = {}

def  extract_data(file):
    global global_data
    file_path = f'{folder}{file}'
    data = pd.read_excel(file_path).fillna('').to_dict() 
    global_data = data
    
def create_recordIdentifiers():
    try:
        id = global_data.get("Record Identifier ID")
        record = global_data.get("System Name")
        code = global_data.get("Code")
        starting = global_data.get("Starting")
        description = global_data.get("System Description")
        next = global_data.get("Next")
        rList = list(id.keys())
        for x in rList:
            record_id = id.get(x)
            rName = record.get(x)
            desc = description.get(x)
            cod = code.get(x)
            nxt = next.get(x) 
            start = starting.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sel_rec = RecordIdentifiers.objects.filter(id = record_id,record = rName)
            if not sel_rec:
                RecordIdentifiers.objects.create(id = record_id,record = rName,next = nxt,description = desc,code=cod,starting = start,created_by_id = user)
    except Exception as e:
        print(e)

def create_selectors():
    try:
        id = global_data.get("Selector ID")
        system_name = global_data.get("System Name")
        type = global_data.get("Type")
        description = global_data.get("System Description")
        sList = list(system_name.keys())
        lang = Language.objects.get(system_name='English (US)')
        for x in sList:
            sel_id = id.get(x)
            sName = system_name.get(x)
            typ = type.get(x)
            desc = description.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sel_rec = Selectors.objects.filter(id = sel_id,system_name = sName)
            check=Translation.objects.filter(label=sName, language_id=lang.id)
            if not check:
                trans_id = get_rid_pkey('translation')
                Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
            label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            if not sel_rec:
                Selectors.objects.create(id = sel_id,system_name = sName,type = typ,description = desc,created_by_id = user)
            sel = Selectors.objects.get(id = sel_id)
            updatenextid('selectors',sel.id)
            trans = TranslationSelector.objects.filter(selector=sel, translation_id=label_rec.id)
            if not trans:
                TranslationSelector.objects.create(selector=sel, translation = label_rec)
    except Exception as e:
        print(e)
        
def create_choice():
    try:
        selector = global_data.get('Selector')
        sel_id = global_data.get("Selector ID")
        system_name = global_data.get('System Name')
        id = global_data.get("Choice ID")
        seq = global_data.get("Sequence")
        description = global_data.get("System Description")
        lang = Language.objects.get(system_name='English (US)')
        sList = list(selector.keys())
        for x in sList:
            choice_id = id.get(x)
            nName = system_name.get(x)
            sel = selector.get(x)
            sequence = int(seq.get(x))
            desc = description.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            gSel = Selectors.objects.filter(system_name=sel).first()
            choice_rec = Choice.objects.filter(system_name=nName,id = choice_id)
            check=Translation.objects.filter(label=nName, language_id=lang.id)
            if not check:
                trans_id = get_rid_pkey('translation')
                Translation.objects.create(id=trans_id,label=nName, language_id=lang.id)
            label_rec = Translation.objects.get(label=nName, language_id=lang.id)
            if not choice_rec:
                Choice.objects.create(id = choice_id,selector=gSel,system_name=nName,sequence=sequence,description = desc,created_by_id = user)
            ch = Choice.objects.get(id = choice_id)
            updatenextid('choice',ch.id)
            trans = TranslationChoice.objects.filter(choice=ch, translation_id=label_rec.id)
            if not trans:
                TranslationChoice.objects.create(choice=ch, translation = label_rec)
    except Exception as e:
        print(e)
  
def create_dataset():
    try:
        id = global_data.get("Dataset ID")
        system_name = global_data.get('System Name')
        description = global_data.get('System Description')
        dList = list(system_name.keys())
        for x in dList:
            tbl_id = id.get(x)
            dName = system_name.get(x)
            desc = description.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            dataset_rec = DataTable.objects.filter(id= tbl_id,system_name=dName)
            if not dataset_rec:
                DataTable.objects.create(id= tbl_id,system_name=dName,description=desc,created_by_id = user)
                updatenextid('datatable',tbl_id)
    except Exception as e:
        print(e)

def create_data():
    try:
        id = global_data.get("Data ID")
        d_id = global_data.get("Dataset ID")
        data_source = global_data.get('Dataset')
        seq= global_data.get("Sequence")
        system_name = global_data.get('Data System Name')
        #data_type =global_data.get('Data Type')
        description = global_data.get('System Description')
        #field = global_data.get('Field')
        #field_type = global_data.get('Field Type')
        #comment= global_data.get('Comment')
        lang = Language.objects.get(system_name='English (US)')
        dList = list(system_name.keys())
        for x in dList:
            data_id = id.get(x)
            dName = system_name.get(x)
            desc = description.get(x)
            dset=data_source.get(x)
            temp_sequence= seq.get(x)
            if temp_sequence == '':
                sequence= None
            else:
                sequence = int(temp_sequence)
            #dt = data.get(x)
            #dtype=data_type.get(x)
            #f = field.get(x)
            #ftype = field_type.get(x)
            #cmnt = comment.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sdset = DataTable.objects.get(system_name=dset)
            try:
                check=Translation.objects.filter(label=dName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=dName, language_id=lang.id)
                label_rec = Translation.objects.get(label=dName, language_id=lang.id)
            except Exception as e:
                print(e)
            data_rec = Data.objects.filter(id = data_id,system_name=dName)
            if not data_rec:
                Data.objects.create(id = data_id,system_name=dName,description=desc,data_source=sdset,created_by_id = user,sequence=sequence)#data_type=dtype,field= f,field_type=ftype,comment=cmnt,)
            dt_id = Data.objects.get(id = data_id)
            updatenextid('data',dt_id.id)
            trans = TranslationData.objects.filter(name=dt_id, translation_id=label_rec.id)
            if not trans:
                TranslationData.objects.create(name=dt_id, translation = label_rec)
    except Exception as e:
        print(e)
     
def create_icons():
    try:
        id = global_data.get("Icon ID")
        system_name = global_data.get('System Name')
        icon_image = global_data.get('Image File')
        lang = Language.objects.get(system_name='English (US)')
        iList = list(system_name.keys())
        for x in iList:
            icon_id = id.get(x)
            sName = system_name.get(x)
            iImage = icon_image.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            icon_rec = Icons.objects.filter(id =icon_id,system_name=sName)
            try:
                check=Translation.objects.filter(label=sName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
                label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            except Exception as e:
                print(e)
            if not icon_rec:
                Icons.objects.create(id =icon_id,system_name=sName,icon_image=iImage,created_by_id = user)
            ic_id = Icons.objects.get(id = icon_id)
            updatenextid('icons',ic_id.id)
            trans = TranslationIcons.objects.filter(icon=ic_id, translation_id=label_rec.id)
            if not trans:
                TranslationIcons.objects.create(icon=ic_id, translation = label_rec)
    except Exception as e:
        print(e)
        
        
def create_conf():
    try:
        id = global_data.get("Configuration ID")
        system_name = global_data.get('System Name')
        type = global_data.get('Type')
        default_value = global_data.get("Default Color")
        lang = Language.objects.get(system_name='English (US)')
        #editable = data.get("Editable")
        confList = list(system_name.keys())
        for x in confList:
            conf_id = id.get(x)
            conf = system_name.get(x)
            typ = type.get(x)
            #edit = editable.get(x)
            # if edit == 'yes' or 'Yes':
            #     edit = True
            # else:
            #     edit = False
            vdef = default_value.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            conf_rec = Configuration.objects.filter(id = conf_id,system_name=conf)
            try:
                check=Translation.objects.filter(label=conf, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=conf, language_id=lang.id)
                label_rec = Translation.objects.get(label=conf, language_id=lang.id)
            except Exception as e:
                print(e)
            if  not conf_rec:
                Configuration.objects.create(id = conf_id,system_name=conf,type = typ,default_value =vdef,created_by_id = user)
            config_id = Configuration.objects.get(id = conf_id)
            updatenextid('data',config_id.id)
            trans = TranslationConfiguration.objects.filter(configuration=config_id, translation_id=label_rec.id)
            if not trans:
                TranslationConfiguration.objects.create(configuration=config_id, translation = label_rec)
    except Exception as e:
        print(e)
        
        
def create_currencies():
    try:
        id = global_data.get("Currency ID")
        system_name = global_data.get('System Name')
        code = global_data.get('Code')
        sym = global_data.get("Symbol")
        lang = Language.objects.get(system_name='English (US)')
        sList = list(system_name.keys())
        for x in sList:
            cur_id = id.get(x)
            xName = system_name.get(x)
            xCode = code.get(x)
            xSym = sym.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            cur_rec = Currency.objects.filter(id = cur_id,system_name=xName)
            try:
                check=Translation.objects.filter(label=xName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=xName, language_id=lang.id)
                label_rec = Translation.objects.get(label=xName, language_id=lang.id)
            except Exception as e:
                print(e)
            if not cur_rec:
                Currency.objects.create(id = cur_id,system_name=xName,code=xCode,symbol=xSym,created_by_id = user)
            curr_id = Currency.objects.get(id = cur_id)
            updatenextid('currency',curr_id.id)
            trans = TranslationCurrency.objects.filter(currency=curr_id, translation_id=label_rec.id)
            if not trans:
                TranslationCurrency.objects.create(currency=curr_id, translation = label_rec)
    except Exception as e:
        print(e)
        
def create_countries():
    try:
        id = global_data.get("Country ID")
        native_name = global_data.get('Native Name')
        telephone_code = global_data.get("Telephone Code")
        currency = global_data.get('Currency Name')
        country = global_data.get("Country Code")
        cur_code = global_data.get("Currency Code")
        #cur_id = data.get("Currency ID")
        symbol_position = global_data.get("Currency Symbol Position")
        money_format = global_data.get('Money Format',"")
        date_format = global_data.get("Date Format","")
        #time_format = data.get("Time Format","")
        time_id = global_data.get("Time Choice ID")
        #symbol_id = data.get("Symbol Choice ID")
        conList = list(country.keys())
        for x in conList:
            con_id = id.get(x)
            t_id = time_id.get(x)
            country_code = country.get(x)
            #s_id = symbol_id.get(x)
            cu_code =cur_code.get(x)
            #cu_id = cur_id.get(x)
            nName = native_name.get(x)
            xtel= telephone_code.get(x)
            xCurr = currency.get(x)
            sym = symbol_position.get(x)
            Mon= money_format.get(x)
            Date = date_format.get(x)
            #Time = time_format.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sCur = Currency.objects.filter(code=cu_code,system_name =xCurr).first()
            sSym = Choice.objects.filter(system_name=sym).first()
            sMon = Choice.objects.filter(system_name=Mon).first()
            sDate = Choice.objects.filter(system_name=Date).first()
            sTime = Choice.objects.filter(id  = t_id).first()
            con_rec = Country.objects.filter(id = con_id,country = country_code)
            if not con_rec:
                Country.objects.create(id = con_id,native_name=nName,telephone_code=xtel,currency=sCur,symbol_position=sSym,
                                       money_format=sMon,date_format=sDate,time_format = sTime,country = country_code,created_by_id = user)
                updatenextid('country',con_id)
    except Exception as e:
        print(e)
        
def create_state():
    try:
        id = global_data.get("State ID")
        abbreviation = global_data.get('Code')
        country = global_data.get("Country Code")
        con_id = global_data.get("Country ID")
        system_name = global_data.get('System Name')
        seq = global_data.get("Sequence")
        sList = list(system_name.keys())
        for x in sList:
            s_id = id.get(x)
            c_code = country.get(x)
            abb = abbreviation.get(x)
            sName=system_name.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            scon = Country.objects.filter(country=c_code).first()
            sequence = int(seq.get(x))
            state_rec = State.objects.filter(id = s_id,system_name= sName)
            if not state_rec:
                State.objects.create(id = s_id,abbreviation = abb,country=scon,system_name = sName,sequence = sequence, created_by_id = user)
                updatenextid('state',s_id)
    except Exception as e:
        print(e)
        
def create_language():
    try:
        id = global_data.get("Language ID")
        system_name = global_data.get('System Name')
        #native_Translation = global_data.get('Native Name')
        #code = global_data.get("Code")
        #direction = global_data.get("Direction")
        #dir_choice = global_data.get("Direction Choice ID")
        langList = list(system_name.keys())
        for x in langList:
            l_id =  id.get(x)
            xName = system_name.get(x)
            #dir_c = dir_choice.get(x)
            #nTrans = native_Translation.get(x)
            #cod = code.get(x)
            #dir = direction.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            #sChoice = Choice.objects.filter(id=dir_c).first()
            lang_rec =Language.objects.filter(id =l_id,system_name=xName)
            if not lang_rec:
                Language.objects.create(id =l_id,system_name=xName,created_by_id = user)
                updatenextid('language',l_id)
    except Exception as e:
        print(e)
        
def create_list():
    try:
        id = global_data.get("List ID")
        system_name = global_data.get('System Name')
        tbl_id = global_data.get("Dataset ID")
        #category = global_data.get('Category')
        data_source = global_data.get("Dataset")
        description = global_data.get("System Description")
        view_id = global_data.get("View Choice ID")
        list_type = global_data.get('List Type')
        default_view = global_data.get("Default View")
        icon = global_data.get("Icon System Name")
        icon_id = global_data.get("Icon ID")
        primary = global_data.get("Primary Form")
        type_id = global_data.get("Type Choice ID")
        lang = Language.objects.get(system_name='English (US)')
        lList = list(system_name.keys())
        for x in lList:
            #v_id = view_id.get(x)
            #d_id = tbl_id.get(x)
            l_id = id.get(x)
            desc = description.get(x)
            def_view = default_view.get(x)
            i_name = icon.get(x)
            #i_id = icon_id.get(x)
            #p_form = primary.get(x)
            lName = system_name.get(x)
            ptable = data_source.get(x)
            #cat = category.get(x)
            #t_id = type_id.get(x)
            ltype = list_type.get(x)
            #gccat= Choice.objects.get_or_create(choice_name= cat)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sptble = DataTable.objects.filter(system_name=ptable).first()
            sltp = Choice.objects.filter(system_name = ltype).first()
            list_rec = List.objects.filter(id = l_id,system_name=lName)
            try:
                check=Translation.objects.filter(label=lName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=lName, language_id=lang.id)
                label_rec = Translation.objects.get(label=lName, language_id=lang.id)
            except Exception as e:
                print(e)
            if not list_rec:
                List.objects.create(id = l_id,system_name=lName, data_source=sptble,list_type =sltp,description = desc,default_view = def_view,created_by_id = user)
            list_id = List.objects.get(id = l_id)
            updatenextid('list',list_id.id)
            trans = TranslationList.objects.filter(list=list_id, translation_id=label_rec.id)
            if not trans:
                TranslationList.objects.create(list=list_id, translation = label_rec)
            # form_rec= FormList.objects.filter(primary = p_form)
            # if not form_rec:
            #     FormList.objects.create(
            #         primary = p_form
            #     )
            gicon = Icons.objects.filter(system_name=i_name).first()
            lIcon_rec = ListIcon.objects.filter(list_id = l_id,icon =gicon)
            if  not lIcon_rec:
                ListIcon.objects.create(
                    list_id = l_id,
                    icon =gicon
                )
                
    except Exception as e:
        print(e)
        
def create_menu():
    try:
        id = global_data.get("Menu Item ID")
        system_name = global_data.get("System Name")
        menu_category = global_data.get('Category')
        #description = global_data.get("System Description")
        seq = global_data.get('Sequence')
        lists = global_data.get('List')
        listID = global_data.get("List ID")
        visibility = global_data.get('Visibility')
        lang = Language.objects.get(system_name='English (US)')
        lList = list(system_name.keys())
        for x in lList:
            menu_id= id.get(x)
            mName = system_name.get(x)
            cCat =menu_category.get(x)
            #desc=description.get(x)
            list_name = lists.get(x)
            sequence = int(seq.get(x))
            #vis = visibility.get(x)
            #lst = listID.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            sclist= List.objects.filter(system_name=list_name).first()
            #svis = Choice.objects.filter(choice_name=vis).first()
            sCat = Choice.objects.filter(system_name=cCat).first()
            menu_rec = Menu.objects.filter( id = menu_id,system_name=mName)
            try:
                check=Translation.objects.filter(label=mName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=mName, language_id=lang.id)
                label_rec = Translation.objects.get(label=mName, language_id=lang.id)
            except Exception as e:
                print(e)
            if not menu_rec:
                Menu.objects.create(id = menu_id,list= sclist,system_name=mName,menu_category=sCat,sequence = sequence,created_by_id = user)
            m_id = Menu.objects.get(id = menu_id)
            updatenextid('menu',m_id.id)
            trans = TranslationMenu.objects.filter(menu=m_id, translation_id=label_rec.id)
            if not trans:
                TranslationMenu.objects.create(menu=m_id, translation = label_rec)
    except Exception as e:
        print(e)
        
    
def create_columns():
    try:
        id = global_data.get("Column ID")
        col_list = global_data.get('List')
        #l_id = data.get("List ID")
        column = global_data.get('System Name')
        #seq = global_data.get("Sequence")
        #dataset=global_data.get('Dataset')
        #d_id =global_data.get("Dataset ID")
        visibility = global_data.get('Visibility')
        #data_id = global_data.get("Data ID")
        #data = global_data.get('Data System Name')
        lang = Language.objects.get(system_name='English (US)')
        sList = list(col_list.keys())
        for x in sList:
            col_id =id .get(x) 
            #tbl_id = d_id.get(x)
            #dt_id =data_id.get(x)
            cl = col_list.get(x)
            col = column.get(x)
            #dts = dataset.get(x)
            vsb= visibility.get(x)
            # temp_sequence= seq.get(x)
            # if temp_sequence == '':
            #     sequence= None
            # else:
            #     sequence = int(temp_sequence)
            #dt = data.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            gclist = List.objects.filter(system_name=cl).first()
            gcvsb = Choice.objects.filter(system_name=vsb).first()
            #gctble = DataTable .objects.filter(table=dts).first()
            #gcdata = Data.objects.filter(name=dt).first()
            col_rec= Column.objects.filter(id = col_id,column = col)
            try:
                check=Translation.objects.filter(label=col, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=col, language_id=lang.id)
                label_rec = Translation.objects.get(label=col, language_id=lang.id)
            except Exception as e:
                print(e)
            if not col_rec:
                Column.objects.create(id = col_id,col_list = gclist,column = col,visibility = gcvsb,created_by_id = user)
            column_id = Column.objects.get(id = col_id)
            updatenextid('column',column_id.id)
            trans = TranslationColumn.objects.filter(column=column_id, translation_id=label_rec.id)
            if not trans:
                TranslationColumn.objects.create(column=column_id, translation_id = label_rec.id)
    except Exception as e:
        print(e)
        
def create_forms():
    try:
        system_name = global_data.get('System Name')
        description=global_data.get("System Description")
        #icon = data.get("Icon")
        id = global_data.get("Form ID")
        #icon_id = data.get("Icon ID")
        lang = Language.objects.get(system_name='English (US)')
        fList = list(system_name.keys())
        for x in fList:
            nName = system_name.get(x)
            desc = description.get(x)
            formId = id.get(x)
            #ic_id = icon_id.get(x)
            #icn= icon.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            form_rec = Form.objects.filter(id = formId)
            try:
                check=Translation.objects.filter(label=nName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=nName, language_id=lang.id)
                label_rec = Translation.objects.get(label=nName, language_id=lang.id)
            except Exception as e:
                print(e)
            if len(form_rec) < 1:
                Form.objects.create(id = formId,system_name=nName,description = desc,created_by_id = user)
            form_id = Form.objects.get(id = formId)
            updatenextid('form',form_id.id)
            trans = TranslationForm.objects.filter(form=form_id, translation_id=label_rec.id)
            if not trans:
                TranslationForm.objects.create(form=form_id, translation_id = label_rec.id)
            # if id is not None and icon is not None:
            # form_icon = Form.objects.filter(form=nName).first()
            # gicon = Icons.objects.filter(system_name = icn).first()
            # formIcon_rec= FormIcon.objects.filter()
            # if len(formIcon_rec) < 1:
            #     FormIcon.objects.create(
                    
            #         icon_id=ic_id,
            #         form =form_icon,
            #         icon=gicon
            #     )
    except Exception as e:
        print(e)

def create_stages():
    try:
        id = global_data.get("Form Stage ID")
        form = global_data.get("Form")
        form_id = global_data.get("Form ID")
        system_name = global_data.get("System Name")
        seq = global_data.get("Sequence")
        #warning_interval = global_data.get("Warning Interval")
        #urgent_interval = global_data.get("Urgent Interval")
        lang = Language.objects.get(system_name='English (US)')
        sList = list(system_name.keys())
        for x in sList:
            s_id = id.get(x)
            frm = form.get(x)
            fm_id = form_id.get(x) 
            sName = system_name.get(x)
            temp_sequence= seq.get(x)
            if temp_sequence == '':
                sequence= None
            else:
                sequence = int(temp_sequence)
            #wINT = warning_interval.get(x)
            #uINT = urgent_interval.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            gfrm = Form.objects.filter(system_name = frm).first()
            stage_rec = Stage.objects.filter(id = s_id, system_name = sName,)
            try:
                check=Translation.objects.filter(label=sName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
                label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            except Exception as e:
                print(e)
            if len(stage_rec)<1:
                Stage.objects.create(id = s_id,system_name = sName,form = gfrm,form_id = fm_id,created_by_id = user,sequence=sequence)
            stage_id = Stage.objects.get(id = s_id)
            updatenextid('stage',stage_id.id)
            trans = TranslationStage.objects.filter(stage=stage_id, translation_id=label_rec.id)
            if not trans:
                TranslationStage.objects.create(stage=stage_id, translation_id = label_rec.id)    
    except Exception as e:
        print(e)

def create_entities():
    try:
        id = global_data.get("Entity ID")
        name = global_data.get("System Name")
        parent = global_data.get("Parent Name")
        parent_id = global_data.get("Parent ID")
        eList = list(name.keys())
        for x in eList:
            ent_id = id.get(x)
            eName = name.get(x)
            prnt = parent.get(x)
            prnt_id = parent_id.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            gcprnt = Entity.objects.filter(name=prnt).first()
            entity_rec = Entity.objects.filter(name = eName,id = ent_id)
            if len(entity_rec) < 1:
                Entity.objects.create(id = ent_id,name = eName,parent = gcprnt,created_by_id = user)
                updatenextid('entity',ent_id)
    except Exception as e:
        print(e)

def create_container():
    try:
        id = global_data.get("Container ID")
        container = global_data.get("System Name")
        dimension_1 = global_data.get("Dimension 1")
        dimension_2 = global_data.get("Dimension 2")
        dimension_3 = global_data.get("Dimension 3")
        weight = global_data.get("Weight")
        sur = global_data.get("Surcharge")
        description = global_data.get("System Description")
        lang = Language.objects.get(system_name='English (US)')
        #stage = data.get("")
        #status_choice_id = data.get("")
        cList = list(container.keys())
        for x in cList:
            cont_id = id.get(x)
            cont= container.get(x)
            dim_1 = dimension_1.get(x)
            dim_2 = dimension_2.get(x)
            dim_3 = dimension_3.get(x)
            #surcharge = sur.get(x)
            wt = weight.get(x)
            desc = description.get(x)
            user= User.objects.filter(username = 'admin').values()[0]["id"]
            cont_rec = ContainerTypes.objects.filter(id = cont_id,container = cont)
            try:
                check=Translation.objects.filter(label=cont, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=cont, language_id=lang.id)
                label_rec = Translation.objects.get(label=cont, language_id=lang.id)
            except Exception as e:
                print(e)
            if not cont_rec:
                ContainerTypes.objects.create(id = cont_id,container = cont,dimension_1 = dim_1,dimension_2 = dim_2,dimension_3 = dim_3,weight = wt,created_by_id = user,description = desc)
            con_id = ContainerTypes.objects.get(id = cont_id)
            updatenextid('containertypes',con_id.id)
            trans = TranslationContainerType.objects.filter(containerType=con_id, translation_id=label_rec.id)
            if not trans:
                TranslationContainerType.objects.create(containerType=con_id, translation_id = label_rec.id)  
    except Exception as e:
        print(e)
        
class Command(BaseCommand):
    help = "load data from import excel sheet"
    def handle(self, *args, **kwargs):
        global global_data
        file1 = open('./managementCommandsFiles/managementSequence.txt', 'r') 
        Lines = file1.readlines() 
        for line in Lines:
            line=line.strip('\n')
            if line !='':
                file_method=line.split("|")
                #getting file name
                fileName=file_method[0]
                if fileName in files:
                    extract_data(fileName)
                    #storing method name
                    methName=file_method[1] + "()" 
                    result = eval(methName)
                else:
                    print("File Not found", fileName)