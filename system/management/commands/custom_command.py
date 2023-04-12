# Custom Command to seed database with basic data for further operations.
from django.core.management.base import BaseCommand
from warehouse.models import ContainerTypes,Accounts
from system.models import Choice,DataRequirements,Button,RecordIdentifiers,Selectors,FormSection,FormData,DataSelector,FormList,Currency,Country,State,Configuration,Language,Icons,List,DataTable,Data,Entity,Menu,Column,Form,Stage,Entity,FormList,ListIcon
import pandas as pd
import os
from system.models.translations import TranslationSelector,TranslationChoice,TranslationColumn,TranslationForm,TranslationStage,TranslationList,TranslationMenu,TranslationData,TranslationIcons,TranslationCurrency,TranslationConfiguration,TranslationContainerType,Translation
from system.models.common import FormStage  ,FormPanels
from system.service import get_rid_pkey, updatenextid
from django.contrib.auth.models import User
from system import utils
from django.db.models import Q

# Excel Data path to be import in db
folder = r'./managementcmdfiles/'
files = os.listdir(folder)

# Icon location
icons = r'icon_images/'
imag_file= os.listdir(icons)

# Country flag location
flag_path = r'country_flag/'
flag_file= os.listdir(flag_path)

data_dict={}
global_data = {}

# Get user 
user= User.objects.filter(username = 'admin').values()[0]["id"]

# Function to extract data from excel file
def  extract_data(file):
    global global_data
    file_path = f'{folder}{file}'
    data = pd.read_excel(file_path).fillna('').to_dict() 
    global_data = data

# Function to seed recordidentifier model     
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
            sel_rec = RecordIdentifiers.objects.filter(id = record_id,record = rName)
            if not sel_rec:
                RecordIdentifiers.objects.create(id = record_id,record = rName,next = nxt,description = desc,code=cod,starting = start,created_by_id = user)
    except Exception as e:
        #print("RID Error >", str(e))
        pass

# Function to seed Selectors model           
def create_selectors():
    try:
        trans_id = get_rid_pkey('language')
        lang = Language.objects.get_or_create(id = trans_id,system_name='English (US)')
    except Exception as e:
        print(e)
    try:
        id = global_data.get("Selector ID")
        system_name = global_data.get("System Name")
        type = global_data.get("Type")
        description = global_data.get("System Description")
        lang = Language.objects.get(system_name='English (US)')
        sList = list(system_name.keys())
        for x in sList:
            sel_id = id.get(x)
            sName = system_name.get(x)
            sel_name = utils.encode_api_name(sName)
            typ = type.get(x)
            #desc = description.get(x)
            sel_rec = Selectors.objects.filter(id = sel_id,system_name = sel_name)
            check=Translation.objects.filter(label=sName, language_id=lang.id)
            if not check:
                trans_id = get_rid_pkey('translation')
                Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
            label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            if not sel_rec:
                Selectors.objects.create(id = sel_id,system_name = sel_name,type = typ,created_by_id = user)
            sel = Selectors.objects.get(id = sel_id)
            updatenextid('selectors',sel.id)
            trans = TranslationSelector.objects.filter(selector=sel, translation_id=label_rec.id)
            if not trans:
                TranslationSelector.objects.create(selector=sel, translation = label_rec)
    except Exception as e:
        #print("Selector Error >", str(e))
        pass

# Function to seed Choice model           
def create_choice():

    selector = global_data.get('Selector')
    sel_id = global_data.get("Selector ID")
    system_name = global_data.get('System Name')
    id = global_data.get("Choice ID")
    seq = global_data.get("Sequence")
    #description = global_data.get("System Description")
    lang = Language.objects.get(system_name='English (US)')
    sList = list(selector.keys())
    for x in sList:
        try:
            choice_id = id.get(x)
            nName = utils.encode_api_name(system_name.get(x))
            sel = selector.get(x)
            sel_name = utils.encode_api_name(sel)
            temp_sequence=seq.get(x)
            if nName:
                if temp_sequence == '':
                    sequence= None
                else:
                    sequence = int(temp_sequence)
                gSel = Selectors.objects.filter(system_name=sel_name).first()
                choice_rec = Choice.objects.filter(selector__system_name=sel_name, system_name=nName)
                label = utils.decode_api_name(nName)
                check=Translation.objects.filter(label=label, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=label, language_id=lang.id)
                label_rec = Translation.objects.get(label=label, language_id=lang.id)
                if not choice_rec:
                    Choice.objects.create(id = choice_id,selector=gSel,system_name=nName,sequence=sequence,created_by_id = user)
                ch = Choice.objects.get(id = choice_id)
                updatenextid('choice',ch.id)
                trans = TranslationChoice.objects.filter(choice=ch, translation_id=label_rec.id)
                if not trans:
                    TranslationChoice.objects.create(choice=ch, translation = label_rec)
        except Exception as e:
            #print("Choice Error >", str(e))
            pass

# Function to seed DataSet model     
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
            dataset_rec = DataTable.objects.filter(id= tbl_id,system_name=dName)
            if not dataset_rec:
                DataTable.objects.create(id= tbl_id,system_name=dName,description=desc,created_by_id = user)
                updatenextid('datatable',tbl_id)
    except Exception as e:
        #print("Dataset Error >", str(e))
        pass

# Function to seed Data model   
def create_data():
    try:
        id = global_data.get("Data ID")
        d_id = global_data.get("Dataset ID")
        data_source = global_data.get('Dataset')
        linked_ds=global_data.get('Link Dataset')
        linked_data=global_data.get('Linked Data')
        linked_data_id=global_data.get("Link Data ID")
        seq= global_data.get("Sequence")
        system_name = global_data.get('Data System Name')
        sel_id = global_data.get("Selector ID")
        #disp_data =global_data.get('Linked Data')
        description = global_data.get('System Description')
        field = global_data.get('Field')
        field_type = global_data.get('DTYPE')
        data_type=global_data.get("Data Type")
        #comment= global_data.get('Comment')
        lang = Language.objects.get(system_name='English (US)')
        sel=global_data.get("Selector")
        dList = list(system_name.keys())
        for x in dList:
            data_id = int(id.get(x))
            tempselector_id = sel_id.get(x)
            if tempselector_id == '':
                selector_id=None
            else:
                selector_id= int(tempselector_id)
            ldata=linked_data.get(x)
            dName = system_name.get(x)
            desc = description.get(x)
            dset=data_source.get(x)
            templink_tbl=linked_ds.get(x)
            if templink_tbl == '':
                link_tbl=None
            else:
                link_tbl=templink_tbl
            dt_type=data_type.get(x)
            templink_dt=linked_data_id.get(x)
            if templink_dt == '':
                link_dt=None
            else:
                link_dt=int(templink_dt)
            temp_sequence= seq.get(x)
            #selt=sel.get(x)
            if temp_sequence == '':
                sequence= None
            else:
                sequence = int(temp_sequence)
            f = field.get(x)
            if dName:
                try:
                    ftype = utils.encode_api_name(field_type.get(x))
                    gftype= Choice.objects.filter(system_name=ftype).first()
                    gldt = None
                    gltble = None
                    if link_tbl and link_dt:
                        gltble=DataTable.objects.filter(system_name=link_tbl).first()
                        gldt=Data.objects.filter(data_source=gltble,system_name=ldata).first()
                        if not gldt: gldt= Data.objects.create(id=link_dt,data_source=gltble,system_name=ldata)
                    gsel_id = Selectors.objects.filter(id =selector_id ).first()
                    sdset = DataTable.objects.filter(system_name=dset).first()
                    try:
                        check=Translation.objects.filter(label=dName, language_id=lang.id)
                        if not check:
                            trans_id = get_rid_pkey('translation')
                            Translation.objects.create(id=trans_id,label=dName, language_id=lang.id)
                        label_rec = Translation.objects.get(label=dName, language_id=lang.id)
                    except:
                        pass
                    data_rec = Data.objects.filter(data_source = sdset, system_name=dName)
                    if data_rec:
                        data_rec.update(field=f,field_type=gftype,description=desc,created_by_id = user,sequence=sequence)
                    else:
                        Data.objects.create(id = data_id,linked_ds=gltble,linked_data=gldt,data_type=dt_type,system_name=dName,field=f,field_type=gftype,description=desc,data_source=sdset,created_by_id = user,sequence=sequence)
                        updatenextid('data',data_id)
                    dt_id = Data.objects.get(id = data_id)    
                    trans = TranslationData.objects.filter(name=dt_id, translation_id=label_rec.id)
                    if not trans:
                        TranslationData.objects.create(name=dt_id, translation = label_rec)
                    datasel = DataSelector.objects.filter(selector=gsel_id, data=data_id)
                    if not datasel:
                        if gsel_id and dt_id:
                            DataSelector.objects.create(selector=gsel_id, data=dt_id)
                except Exception as e:
                    print(str(e))
    except Exception as e:
        print("Data Error >", str(e))
        pass

# Function to seed Icons model        
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
            icon_rec = Icons.objects.filter(id =icon_id,system_name=sName)
            try:
                check=Translation.objects.filter(label=sName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
                label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            except:
                pass
            if not icon_rec:
                if iImage in imag_file:
                    icon_p= f'{icons}{iImage}'
                    Icons.objects.create(id =icon_id,system_name=sName,icon_image=icon_p,created_by_id = user)
            ic_id = Icons.objects.get(id = icon_id)
            updatenextid('icons',ic_id.id)
            trans = TranslationIcons.objects.filter(icon=ic_id, translation_id=label_rec.id)
            if not trans:
                TranslationIcons.objects.create(icon=ic_id, translation = label_rec)
    except Exception as e:
        #print("Icons Error >", str(e))
        pass

# Function to seed Configurations model                  
def create_conf():
    try:
        id = global_data.get("Configuration ID")
        system_name = global_data.get('System Name')
        type = global_data.get('Type')
        default_value = global_data.get("Default Color")
        lang = Language.objects.get(system_name='English (US)')
        confList = list(system_name.keys())
        for x in confList:
            conf_id = id.get(x)
            conf = system_name.get(x)
            typ = type.get(x)
            vdef = default_value.get(x)
            conf_rec = Configuration.objects.filter(id = conf_id,system_name=conf)
            try:
                check=Translation.objects.filter(label=conf, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=conf, language_id=lang.id)
                label_rec = Translation.objects.get(label=conf, language_id=lang.id)
            except:
                pass
            if  not conf_rec:
                Configuration.objects.create(id = conf_id,system_name=conf,type = typ,default_value =vdef,created_by_id = user)
            config_id = Configuration.objects.get(id = conf_id)
            updatenextid('data',config_id.id)
            trans = TranslationConfiguration.objects.filter(configuration=config_id, translation_id=label_rec.id)
            if not trans:
                TranslationConfiguration.objects.create(configuration=config_id, translation = label_rec)
    except Exception as e:
        #print("Configurations Error >", str(e))
        pass
        
# Function to seed Currency model           
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
            cur_rec = Currency.objects.filter(id = cur_id,system_name=xName)
            try:
                check=Translation.objects.filter(label=xName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=xName, language_id=lang.id)
                label_rec = Translation.objects.get(label=xName, language_id=lang.id)
            except:
                pass
            if not cur_rec:
                Currency.objects.create(id = cur_id,system_name=xName,code=xCode,symbol=xSym,created_by_id = user)
            curr_id = Currency.objects.get(id = cur_id)
            updatenextid('currency',curr_id.id)
            trans = TranslationCurrency.objects.filter(currency=curr_id, translation_id=label_rec.id)
            if not trans:
                TranslationCurrency.objects.create(currency=curr_id, translation = label_rec)
    except Exception as e:
        #print("Currency Error >", str(e))
        pass

# Function to seed Country model           
def create_countries():
    try:
        id = global_data.get("Country ID")
        native_name = global_data.get('Native Name')
        telephone_code = global_data.get("Telephone Code")
        currency = global_data.get('Currency Name')
        country_code = global_data.get("Country Code")
        system_name = global_data.get('System Name')
        cur_code = global_data.get("Currency Code")
        flag = global_data.get('Flag')
        cur_id = global_data.get("Currency ID")
        symbol_position = global_data.get("Currency Symbol Position")
        money_format = global_data.get('Money Format',"")
        date_format = global_data.get("Date Format","")
        #time_format = global_data.get("Time Format","")
        time_id = global_data.get("Time Choice ID")
        #symbol_id = data.get("Symbol Choice ID")
        conList = list(country_code.keys())
        for x in conList:
            con_id = id.get(x)
            t_id = time_id.get(x)
            ccode = country_code.get(x)
            #s_id = symbol_id.get(x)
            cu_code =cur_code.get(x)
            cu_id = cur_id.get(x)
            nName = native_name.get(x)
            sname = system_name.get(x)
            xtel= telephone_code.get(x)
            xCurr = currency.get(x)
            sym = utils.encode_api_name(symbol_position.get(x))
            Mon= utils.encode_api_name(money_format.get(x))
            Date = utils.encode_api_name(date_format.get(x))
            sflag = flag.get(x)
            sCur = Currency.objects.filter(id = cu_id,code =cu_code).first()
            sSym = Choice.objects.filter(system_name=sym).first()
            sMon = Choice.objects.filter(system_name=Mon).first()
            sDate = Choice.objects.filter(system_name=Date).first()
            sTime = Choice.objects.filter(id  = t_id).first()
            con_rec = Country.objects.filter(id = con_id,country_code = ccode)
            if not con_rec:
                if sflag in flag_file:
                    flag_p= f'{flag_path}{sflag}'
                    Country.objects.create(id = con_id,native_name=nName,telephone_code=xtel,currency=sCur,symbol_position=sSym,
                                        money_format=sMon,date_format=sDate,time_format = sTime,country_code = ccode,
                                        system_name=sname, flag = flag_p, created_by_id = user)
                updatenextid('country',con_id)
    except Exception as e:
        #print("Country Error >", str(e))
        pass

# Function to seed State model           
def create_state():
    try:
        id = global_data.get("State ID")
        abbreviation = global_data.get('Code')
        country_code = global_data.get("Country Code")
        con_id = global_data.get("Country ID")
        system_name = global_data.get('System Name')
        seq = global_data.get("Sequence")
        sList = list(system_name.keys())
        for x in sList:
            s_id = id.get(x)
            c_code = country_code.get(x)
            abb = abbreviation.get(x)
            sName=system_name.get(x)
            scon = Country.objects.filter(country_code=c_code).first()
            sequence = int(seq.get(x))
            state_rec = State.objects.filter(id = s_id,system_name= sName)
            if not state_rec:
                State.objects.create(id = s_id,abbreviation = abb,country=scon,system_name = sName,sequence = sequence, created_by_id = user)
                updatenextid('state',s_id)
    except Exception as e:
        #print("State Error >", str(e))
        pass

# Function to seed Language model           
def create_language():
    try:
        id = global_data.get("Language ID")
        system_name = global_data.get('System Name')
        native_Translation = global_data.get('Native Name')
        code = global_data.get("Code")
       # direction = global_data.get("Direction")
        dir_choice = global_data.get("Direction Choice ID")
        langList = list(system_name.keys())
        for x in langList:
            try:
                l_id =  id.get(x)
                xName = system_name.get(x)
                dir_c = dir_choice.get(x)
                nTrans = native_Translation.get(x)
                cod = code.get(x)
                sChoice = Choice.objects.filter(id=dir_c).first()
                lang_rec =Language.objects.filter(id =l_id,system_name=xName)
                if not lang_rec:
                    Language.objects.create(id =l_id,system_name=xName,native_name=nTrans,code=cod,direction=sChoice,created_by_id = user)
                    updatenextid('language',l_id)
            except Exception as e:
                print(e)
    except Exception as e:
        #print("Language Error >", str(e))
        pass

# Function to seed List model           
def create_list():
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
            try:
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
                ltype = utils.encode_api_name(list_type.get(x))
                #gccat= Choice.objects.get_or_create(choice_name= cat)
                sptble = DataTable.objects.filter(system_name=ptable).first()
                sltp = Choice.objects.filter(system_name = ltype).first()
                list_rec = List.objects.filter(id = l_id,system_name=lName)
                try:
                    check=Translation.objects.filter(label=lName, language_id=lang.id)
                    if not check:
                        trans_id = get_rid_pkey('translation')
                        Translation.objects.create(id=trans_id,label=lName, language_id=lang.id)
                    label_rec = Translation.objects.get(label=lName, language_id=lang.id)
                except:
                    pass
                if not list_rec:
                    if lName:
                        List.objects.create(id = l_id,system_name=lName, data_source=sptble,list_type =sltp,description = desc,default_view = def_view,created_by_id = user)
                list_id = List.objects.get(id = l_id)
                updatenextid('list',list_id.id)
                trans = TranslationList.objects.filter(list=list_id, translation_id=label_rec.id)
                if not trans:
                    TranslationList.objects.create(list=list_id, translation = label_rec)
                gicon = Icons.objects.filter(system_name=i_name).first()
                lIcon_rec = ListIcon.objects.filter(list_id = l_id,icon =gicon)
                if not lIcon_rec:
                    if l_id and gicon: ListIcon.objects.create(list_id = l_id,icon =gicon)
                
            except Exception as e:
                #print("List Error >", str(e))
                pass

# Function to seed Menu model           
def create_menu():
   
    id = global_data.get("Menu Item ID")
    system_name = global_data.get("System Name")
    menu_category = global_data.get('Category')
    seq = global_data.get('Sequence')
    lists = global_data.get('List')
    listID = global_data.get("List ID")
    lang = Language.objects.get(system_name='English (US)')
    lList = list(system_name.keys())
    for x in lList:
        try:
            menu_id= id.get(x)
            mName = system_name.get(x)
            cCat =utils.encode_api_name(menu_category.get(x))
            list_name = lists.get(x)
            sequence = int(seq.get(x))
            sclist= List.objects.filter(system_name=list_name).first()
            sCat = Choice.objects.filter(system_name=cCat).first()
            menu_rec = Menu.objects.filter( id = menu_id,system_name=mName)
            try:
                check=Translation.objects.filter(label=mName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=mName, language_id=lang.id)
                label_rec = Translation.objects.get(label=mName, language_id=lang.id)
            except:
                pass
            if not menu_rec:
                if mName:
                    Menu.objects.create(id = menu_id,list= sclist,system_name=mName,menu_category=sCat,sequence = sequence,created_by_id = user)
            m_id = Menu.objects.get(id = menu_id)
            updatenextid('menu',m_id.id)
            trans = TranslationMenu.objects.filter(menu=m_id, translation_id=label_rec.id)
            if not trans:
                TranslationMenu.objects.create(menu=m_id, translation = label_rec)
        except Exception as e:
            #print("Menu Error >", str(e))
            pass
        
# Function to seed Column model       
def create_columns():
    id = global_data.get("Column ID")
    col_list = global_data.get('List')
    #field=global_data.get("Field")
    #l_id = data.get("List ID")
    column = global_data.get('Column System Name')
    #seq = global_data.get("Sequence")
    dataset=global_data.get('Dataset')
    d_id =global_data.get("Dataset ID")
    visibility = global_data.get('Visibility')
    data_id = global_data.get("Data ID")
    data = global_data.get('Data System Name')
    lang = Language.objects.get(system_name='English (US)')
    sList = list(col_list.keys())
    for x in sList:
        try:
            col_id =id.get(x) 
            #col_field=field.get(x)
            temptbl_id = d_id.get(x)
            if temptbl_id == '':
                tbl_id = None
            else:
                tbl_id = int(temptbl_id)
            tempdt_id =data_id.get(x)
            if tempdt_id == '':
                dt_id= None
            else:
                dt_id = int(tempdt_id)
            cl = col_list.get(x)
            col = column.get(x)
            dts = dataset.get(x)
            vsb= utils.encode_api_name(visibility.get(x))
            # temp_sequence= seq.get(x)
            # if temp_sequence == '':
            #     sequence= None
            # else:
            #     sequence = int(temp_sequence)
            dt = data.get(x)
            gclist = List.objects.filter(system_name=cl).first()
            gcvsb = Choice.objects.filter(selector__system_name='visibility', system_name=vsb).first()
            gctble = DataTable .objects.filter(id =tbl_id).first()
            gcdata = Data.objects.filter(id =dt_id).first()
            col_rec = Column.objects.filter(col_list = gclist,system_name = col)
            try:
                check=Translation.objects.filter(label=col, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=col, language_id=lang.id)
                label_rec = Translation.objects.get(label=col, language_id=lang.id)
            except Exception as e:
                print(e)
            if not col_rec:
                if col and dt:
                    Column.objects.create(id = col_id,col_list = gclist,system_name = col,visibility = gcvsb,col_table=gctble,col_data=gcdata,created_by_id = user)
            column_id = Column.objects.get(id = col_id)
            updatenextid('column',column_id.id)
            trans = TranslationColumn.objects.filter(column=column_id, translation_id=label_rec.id)
            if not trans:
                TranslationColumn.objects.create(column=column_id, translation_id = label_rec.id)
        except Exception as e:
            # print("Column Error >", str(e))
            pass

# Function to seed Forms model   
def create_forms():
    try:
        system_name = global_data.get('Form System Name')
        description=global_data.get("System Description")
        icon = global_data.get("Icon")
        id = global_data.get("Form ID")
        title_id = global_data.get("Title Data ID")
        title=global_data.get("Title Data")
        fileType=global_data.get("Type")
        #icon_id = global_data.get("Icon ID")
        lang = Language.objects.get(system_name='English (US)')
        fList = list(system_name.keys())
        for x in fList:
            nName = system_name.get(x)
            desc = description.get(x)
            formId = id.get(x)
            tempttl_id=title_id.get(x)
            if tempttl_id == '':
                ttl_id = None
            else:
                ttl_id = int(tempttl_id)
            #ic_id = icon_id.get(x)
            icn= icon.get(x)
            ttl=title.get(x)
            fltype=fileType.get(x)
            gtitle=Data.objects.filter(id = ttl_id,system_name=ttl).first()
            gftype=Choice.objects.filter(selector__system_name='price_basis',system_name=fltype).first()
            gicon= Icons.objects.filter(system_name=icn).first()
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
                Form.objects.create(id = formId,system_name=nName,title=gtitle,ftype=gftype,description = desc,created_by_id = user, icon=gicon)
            form_id = Form.objects.get(id = formId)
            updatenextid('form',form_id.id)
            trans = TranslationForm.objects.filter(form=form_id, translation_id=label_rec.id)
            if not trans:
                TranslationForm.objects.create(form=form_id, translation_id = label_rec.id)        
    except Exception as e:
        print("Form Error >", str(e))
        pass

# Function to seed FormList model   
def create_formlist():
    try:
        id=global_data.get("ListForm ID")
        list_id = global_data.get("List ID")
        fName = global_data.get("Form Name")
        form_id = global_data.get("Form ID")
        list_name=global_data.get("List Name")
        cList = list(list_id.keys())
        for x in cList:
            l_id = list_id.get(x)
            flist_id=id.get(x)
            fname= fName.get(x)
            f_id = form_id.get(x)
            lName= list_name.get(x)
            if (fname or f_id) and (lName or l_id):
                glist = List.objects.filter(Q(id=l_id)|Q(system_name=lName)).first()
                gform=Form.objects.filter(Q(id=f_id)|Q(system_name=fname)).first()
                flist_rec = FormList.objects.filter(id = flist_id,list=glist)
                if not flist_rec:
                    FormList.objects.create(id = flist_id,list=glist,form=gform,created_by_id = user)
                    formlist_id = FormList.objects.get(id = flist_id)
                    updatenextid('formlist',formlist_id.id)
    except Exception as e:
        print("FList Error >", str(e))
        pass
    
# Function to seed formpannel model
def create_formpanels():
    try:
        form_id = global_data.get("Form ID")
        list_id=global_data.get("List ID")
        form=global_data.get("Form")
        flist =global_data.get("List")
        position=global_data.get("Position")
        initial_view=global_data.get("Initial View")
        line=global_data.get("Lines")
        #block=global_data.get("Block")
        total_type=global_data.get("Total Type")
        total_column=global_data.get("Total Column")
        fpList = list(form.keys())
        for x in fpList:
            frm=form.get(x)
            fl=flist.get(x)
            #pos=position.get(x)
            l_id=list_id.get(x)
            #init=initial_view.get(x)
            f_id = form_id.get(x)
            #lne=line.get(x)
           # ttype=total_type.get(x)
            #tcolmn=total_column.get(x)
            gform=Form.objects.filter(Q(id =f_id )|Q(system_name=frm)).first()
            gflist=List.objects.filter(Q(id =l_id )|Q(system_name=fl)).first()
            #ginitView=Choice.objects.filter(selector__system_name='form_panel_initial_view',system_name=init).first()
            #gttype=Choice.objects.filter(selector__system_name='form_panel_total_type',system_name=ttype).first()
            #gtcolmn=Column.objects.filter(system_name=tcolmn).first()
            fp_rec=FormPanels.objects.filter(form=frm)
            if not fp_rec:
                FormPanels.objects.create(form=gform,flist=gflist,created_by_id = user)
    except Exception as e:
        print("FPanels Error >", str(e))
        pass
# Function to seed Stage model   
def create_stages():
    try:
        id = global_data.get("Stage ID")
        system_name = global_data.get("System Name")
        lang = Language.objects.get(system_name='English (US)')
        sList = list(system_name.keys())
        for x in sList:
            s_id = id.get(x)
            sName = system_name.get(x)
            stage_rec = Stage.objects.filter(id = s_id)
            try:
                check=Translation.objects.filter(label=sName, language_id=lang.id)
                if not check:
                    trans_id = get_rid_pkey('translation')
                    Translation.objects.create(id=trans_id,label=sName, language_id=lang.id)
                label_rec = Translation.objects.get(label=sName, language_id=lang.id)
            except Exception as e:
                print(e)
            if len(stage_rec)<1:
                Stage.objects.create(id = s_id,system_name = sName,created_by_id = user)
            stage_id = Stage.objects.get(id = s_id)
            updatenextid('stage',stage_id.id)
            trans = TranslationStage.objects.filter(stage=stage_id, translation_id=label_rec.id)
            if not trans:
                TranslationStage.objects.create(stage=stage_id, translation_id = label_rec.id)    
    except Exception as e:
        print("Stage Error >", str(e))
        pass

# Function to seed FormStage model           
def create_formstage():
    try:
        id = global_data.get("Form Stage ID")
        form = global_data.get("Form")
        form_id = global_data.get("Form ID")
        stage = global_data.get("Stage")
        seq = global_data.get("Sequence")
        stage_id=global_data.get("Stage ID")
        sList = list(stage.keys())
        for x in sList:
            fs_id = id.get(x)
            s_id=stage_id.get(x)
            frm = form.get(x)
            f_id = form_id.get(x) 
            sName = stage.get(x)
            temp_sequence= seq.get(x)
            if temp_sequence == '':
                sequence= None
            else:
                sequence = int(temp_sequence)
            if (frm or f_id) and (sName or s_id):
                gform=Form.objects.filter(Q(id =f_id )|Q(system_name=frm)).first()
                stage_rec = Stage.objects.filter(Q(id = s_id)|Q(system_name=sName)).first()
                fs_rec = FormStage.objects.filter(form=gform,stage=stage_rec)
                if not fs_rec:
                    FormStage.objects.create(form = gform, stage=stage_rec, sequence =sequence, 
                                            created_by_id = user)
    except Exception as e:
        print("FStage Error >", str(e))
        pass

# Function to seed FormSection model
def create_formsection():
    try:
        section_id = global_data.get("Section ID")
        sName = global_data.get("System Name")
        form_id = global_data.get("Form ID")
        form_name=global_data.get("Form")
        seq = global_data.get("Sequence")
        visibility=global_data.get("Visible Choice ID")
        visible= global_data.get("Visible")
        fsList = list(form_id.keys())
        for x in fsList:
            fsection = sName.get(x)
            if fsection:
                f_id = form_id.get(x)
                fName= form_name.get(x)
                vis=utils.encode_api_name(visible.get(x))
                temp_sequence= seq.get(x)
                if temp_sequence == '':
                    sequence= None
                else:
                    sequence = int(temp_sequence)
                gvis = Choice.objects.filter(system_name=vis).first()
                gform=Form.objects.filter(id=f_id).first()
                flist_rec = FormSection.objects.filter(section_title=fsection,form=f_id)
                if not flist_rec:
                    FormSection.objects.create(section_title=fsection,form=gform,section_sequence=sequence,created_by_id = user)
            
    except Exception as e:
        print("FSection Error >", str(e))
        pass
    
# Function to seed FormButton model
def create_formbutton():
    try:
        fsbid=global_data.get("Form Stage Button ID")
        form=global_data.get("Form")
        form_id=global_data.get("Form ID")
        stage=global_data.get("Stage")
        stage_id=global_data.get("Stage ID")
        form_button=global_data.get("Form Button")
        form_button_id =global_data.get("Form Button ID")
        sequence=global_data.get("Sequence")
        highlight=global_data.get("Highlight")
        seq=global_data.get("seq")
        Button.objects.filter()
        
    except Exception as e:
        print("Fbutton Error>>", e)
        pass
# Function to seed FormData model        
def create_formdata():
    try:
        fdata= global_data.get("Form Data System Name")
        display_data=global_data.get("Translation")
        form_id = global_data.get("Form ID")
        data_type=global_data.get("Data Type")
        is_heading=global_data.get("Header")
        form=global_data.get("Form")
        table=global_data.get("Dataset")
        visibility = global_data.get("Visibility")
        section=global_data.get("Section")
        column=global_data.get("Column")
        seq=global_data.get("Sequence")
        position=global_data.get("Position")
        lines=global_data.get("Lines")
        fdList=list(fdata.keys())
        for x in fdList:
            dis_data=display_data.get(x)
            fName=form.get(x)
            form_data=fdata.get(x)
            #f_id=form_id.get(x)
            tbl=table.get(x)
            templine=lines.get(x)
            if templine == '':
                fline=None
            else:
                fline=int(templine)
            head=is_heading.get(x)
            valid = ['TRUE', 'true', 'True', 'yes', 'YES', 'Yes']
            if head in valid:
                head = True
            else:
                head =False
            dt_type=utils.encode_api_name(data_type.get(x))
            vis= utils.encode_api_name(visibility.get(x))
            tempsec=section.get(x)
            if tempsec == '':
                sec= None
            else:
                sec = int(tempsec)
            tempos=position.get(x)
            if tempos == '':
                pos= None
            else:
                pos = int(tempos)
            tempcol=column.get(x)
            if tempcol == '':
                col= None
            else:
                col = int(tempcol)
            tempseq=seq.get(x)
            if tempseq == '':
                sequence= None
            else:
                sequence = int(tempseq)
            if fName and tbl and form_data:
                gform=Form.objects.filter(system_name = fName).first()
                gtable=DataTable.objects.filter(system_name=tbl).first()
                gdata=Data.objects.filter(data_source__system_name=tbl, system_name = form_data).first()
                #gdtype=Choice.objects.filter(selector__system_name='data_type',system_name=dt_type).first()
                gvis=Choice.objects.filter(selector__system_name='visibility',system_name=vis).first()
                gsec=FormSection.objects.filter(section_sequence= sec,form=gform).first()
                formdata_rec=FormData.objects.filter(form=gform, table=gtable, data=gdata)
                if not formdata_rec:
                    f_data=get_rid_pkey('formdata')
                    FormData.objects.create(id =f_data,display_label=dis_data,form=gform,table=gtable,
                                            data=gdata,visibility=gvis,section=gsec,column=col,
                                            position=pos,sequence=sequence,created_by_id = user,line=fline)
                
    except Exception as e:
        print("FData Error >", str(e))
        pass
    
def create_fdrequirements():
    try:
        form=global_data.get("Form")
        fId=global_data.get("Form ID")
        fStage=global_data.get("Form Stage")
        fsId=global_data.get("Form Stage ID")
        data=global_data.get("Form Data")
        dId=global_data.get("Data ID ")
        requirement=global_data.get("Requirement")
        reId=global_data.get("Requirement Choice ID")
        fdList = list(form.keys())
        for x in fdList:
            fName=form.get(x)
            fid=fId.get(x)
            fstage=fStage.get(x)
            fsid=fsId.get(x)
            dt=data.get(x)
            d_id=dId.get(x)
            req=requirement.get(x)
            #tempreqId=reId.get(x)
            # if tempreqId == '':
            #     reqId= None
            # else:
            #     reqId = int(tempreqId)
            if fName and fstage and req:
                gform=Form.objects.filter(system_name=fName).first()
                gfstage=Stage.objects.filter(system_name=fstage).first()
                gdata=Data.objects.filter(system_name=dt).first()
                greq=Choice.objects.filter(selector__system_name='data_required',system_name=req).first()
                dreq_rec=DataRequirements.objects.filter(form=gform,data=gdata,stage=gfstage,requirement=greq)
                if not dreq_rec:
                    DataRequirements.objects.create(form=gform,data=gdata,stage=gfstage,requirement=greq,created_by_id = user)
    except Exception as e:
        print("data requirements Error >>",e)

# Function to seed Entity model        
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
            gcprnt = Entity.objects.filter(name=prnt).first()
            entity_rec = Entity.objects.filter(name = eName,id = ent_id)
            if len(entity_rec) < 1:
                Entity.objects.create(id = ent_id,name = eName,parent = gcprnt,created_by_id = user)
                updatenextid('entity',ent_id)
    except Exception as e:
        print("Entity Error >", str(e))
        pass

# Function to seed containerTypes model
# def create_container():
#     try:
#         id = global_data.get("Container ID")
#         container = global_data.get("System Name")
#         dimension_1 = global_data.get("Dimension 1")
#         dimension_2 = global_data.get("Dimension 2")
#         dimension_3 = global_data.get("Dimension 3")
#         weight = global_data.get("Weight")
#         sur = global_data.get("Surcharge")
#         description = global_data.get("System Description")
#         lang = Language.objects.get(system_name='English (US)')
#         #stage = data.get("")
#         #status_choice_id = data.get("")
#         cList = list(container.keys())
#         for x in cList:
#             cont_id = id.get(x)
#             cont= container.get(x)
#             dim_1 = dimension_1.get(x)
#             dim_2 = dimension_2.get(x)
#             dim_3 = dimension_3.get(x)
#             #surcharge = sur.get(x)
#             wt = weight.get(x)
#             desc = description.get(x)
#             user= User.objects.filter(username = 'admin').values()[0]["id"]
#             cont_rec = ContainerTypes.objects.filter(id = cont_id,container = cont)
#             try:
#                 check=Translation.objects.filter(label=cont, language_id=lang.id)
#                 if not check:
#                     trans_id = get_rid_pkey('translation')
#                     Translation.objects.create(id=trans_id,label=cont, language_id=lang.id)
#                 label_rec = Translation.objects.get(label=cont, language_id=lang.id)
#             except Exception as e:
#                 print(e)
#             if not cont_rec:
#                 ContainerTypes.objects.create(id = cont_id,container = cont,dimension_1 = dim_1,dimension_2 = dim_2,dimension_3 = dim_3,weight = wt,created_by_id = user,description = desc)
#             con_id = ContainerTypes.objects.get(id = cont_id)
#             updatenextid('containertypes',con_id.id)
#             trans = TranslationContainerType.objects.filter(containerType=con_id, translation_id=label_rec.id)
#             if not trans:
#                 TranslationContainerType.objects.create(containerType=con_id, translation_id = label_rec.id)  
#     except Exception as e:
#         print("Container Error >", str(e))
#         pass


# Function to seed account model
def create_account():
    try:
       #account=global_data.get("Account ID")
       typ=global_data.get("Type")
       type_id=global_data.get("Type ID")
       category=global_data.get("Category")
       cat_id=global_data.get("Category ID")
       code=global_data.get("Code")
       system_name=global_data.get("System Name")
       #profit_loss_cat=global_data.get("Profit/Loss Category")
       acList=list(system_name.keys())
       for x in acList:
           #acc=account.get(x)
           tp=utils.encode_api_name(typ.get(x))
           typ_id=type_id.get(x)
           cat=utils.encode_api_name(category.get(x))
           ct_id=cat_id.get(x)
           cd=code.get(x)
           acName=system_name.get(x)
           gtype=Choice.objects.filter(selector__system_name='account_type',system_name=tp).first()
           gcatg=Choice.objects.filter(selector__system_name='account_category',system_name =cat).first()
           acc_rec=Accounts.objects.filter(system_name=acName)
           if not acc_rec:
                Accounts.objects.create(system_name=acName,type=gtype,category=gcatg,code=cd,created_by_id = user)
    except Exception as e:
        print("account Error >",e)
        pass
# Function to seed account model
def create_account():
    try:
       #account=global_data.get("Account ID")
       typ=global_data.get("Type")
       type_id=global_data.get("Type ID")
       category=global_data.get("Category")
       cat_id=global_data.get("Category ID")
       code=global_data.get("Code")
       system_name=global_data.get("System Name")
       #profit_loss_cat=global_data.get("Profit/Loss Category")
       acList=list(system_name.keys())
       for x in acList:
           #acc=account.get(x)
           tp=utils.encode_api_name(typ.get(x))
           typ_id=type_id.get(x)
           cat=utils.encode_api_name(category.get(x))
           ct_id=cat_id.get(x)
           cd=code.get(x)
           acName=system_name.get(x)
           gtype=Choice.objects.filter(selector__system_name='account_type',system_name=tp).first()
           gcatg=Choice.objects.filter(selector__system_name='account_category',system_name =cat).first()
           acc_rec=Accounts.objects.filter(system_name=acName)
           if not acc_rec:
                Accounts.objects.create(system_name=acName,type=gtype,category=gcatg,code=cd,created_by_id = user)
    except Exception as e:
        print("account Error >",e)
        pass
# Parent Function for DataBase Seeding        
class Command(BaseCommand):
    help = "load data from import excel sheet"
    def handle(self, *args, **kwargs):
        global global_data
        file1 = open('./managementcmdfiles/managementSequence.txt', 'r') 
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