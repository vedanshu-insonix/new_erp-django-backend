
from django.core.management.base import BaseCommand
from system.models.common import BaseContent
from system.models import Choice, Selectors, Currency,Country,State,Configuration,Language,Icons,List,Table,Dataset,Data,Entity,Category,Menu,Column,Form
import pandas as pd
import os
from rest_framework.response import Response
from system.views import utils

folder = r'/home/prity/Downloads/'
files = os.listdir(folder)
data_dict={}
class Command(BaseCommand):
    help = "load data from import api's "
    

    def handle(self, *args, **kwargs):
        
        for file in files:
            if file.endswith('.xlsx'):
                
                # if file == "choices.xlsx":
                #     data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #     selector = data.get('Selector')
                #     choice_name = data.get('Choice_Name')
                #     seq = data.get("Sequence")
                #     description = data.get("Description")
                #     default = data.get("Default")
                #     sList = list(selector.keys())
                #     for x in sList:
                #         nName = choice_name.get(x)
                #         sel = selector.get(x)
                #         sequence = int(seq.get(x))
                #         desc = description.get(x)
                #         gcSel = Selectors.objects.get_or_create(selector=sel,description=desc)
                #         sSel = Selectors.objects.filter(selector=sel).first()
                #         choice_rec = Choice.objects.filter(selector=sSel)
                #         if choice_rec:
                #             pass
                #         else:
                #             Choice.objects.create(
                #                     selector=sSel,
                #                     choice_name=nName,
                #                     sequence=sequence
                #                 )
                    
                # if file == "new_dataset.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         name = data.get('System Name')
                #         description = data.get('System Description')
                #         entity = data.get("Relation to Entity")
                #         dList = list(name.keys())
                #         for x in dList:
                #             dName = name.get(x)
                #             desc = description.get(x)
                #             ent = entity.get(x)
                #             gcent = Entity.objects.get_or_create(name=ent)
                #             sent = Entity.objects.filter(name=ent).first()
                #             dataset_rec =Dataset.objects.get( name=dName)
                #             if dataset_rec:
                #                 pass
                #             else:
                                
                #                 Dataset.objects.create(
                #                         name=dName,
                #                         description=desc,
                #                         entity=sent
                #                     )
                #     except Exception as e:
                #         print(e)
                        
                # if file == "new_data.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         dataset = data.get('Dataset')
                #         name = data.get('System Name')
                #         data_type =data.get('Data Type')
                #         description = data.get('System Description')
                #         field = data.get('Field')
                #         field_type = data.get('Field Type')
                #         comment= data.get('Comment')
                #         dList = list(name.keys())
                #         for x in dList:
                #             dName = name.get(x)
                #             desc = description.get(x)
                #             dset=dataset.get(x)
                #             dtype=data_type.get(x)
                #             f = field.get(x)
                #             ftype = field_type.get(x)
                #             cmnt = comment.get(x)
                #             gcdset = Dataset.objects.get_or_create(name=dset)
                #             sdset = Dataset.objects.filter(name=dset).first()
                #             data_rec = Data.objects.get(name=dName)
                #             if data_rec:
                #                 pass
                #             else:
                                
                #                 Data.objects.create(
                #                         name=dName,
                #                         description=desc,
                #                         dataset=sdset,
                #                         data_type=dtype,
                #                         field= f,
                #                         field_type=ftype,
                #                         comment=cmnt
                #                     )
                #     except Exception as e:
                #         print(e)
                        
                # if file == "Icon.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         system_name = data.get('System Name')
                #         icon_image = data.get('Image File')
                #         usage = data.get("Usage")
                #         iList = list(system_name.keys())
                #         for x in iList:
                #             sName = system_name.get(x)
                #             iImage = icon_image.get(x)
                #             use = usage.get(x)
                #             icon_rec = Icons.objects.get(system_name=sName)
                #             if icon_rec:
                #                 pass
                #             else:
                                
                #                 Icons.objects.create(
                #                         system_name=sName,
                #                         icon_image=iImage,
                #                         usage=use
                #                     )
                #     except Exception as e:
                #         print(e)
                        
                # if file == "ConfigurationsFeb6.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         configuration = data.get('System Name')
                #         type = data.get('Type')
                #         default_value = data.get("Default Value")
                #         editable = data.get("Editable")
                #         confList = list(configuration.keys())
                #         for x in confList:
                #             conf = configuration.get(x)
                #             tp = type.get(x)
                #             vdef = default_value.get(x)
                #             conf_rec = Configuration.objects.get(configuration=conf)
                #             if  conf_rec:
                #                 pass
                #             else:
                                
                            
                #                 Configuration.objects.create(
                #                         configuration=conf,
                #                         type = tp,
                #                         default_value =vdef
                                        
                #                     )
                #     except Exception as e:
                #         print(e)
                               
                # if file == "CurrenciesFeb6.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         name = data.get('Name')
                #         code = data.get('Code')
                #         sym = data.get("Symbol")
                        
                #         sList = list(name.keys())
                #         for x in sList:
                #             xName = name.get(x)
                #             xCode = code.get(x)
                #             xSym = sym.get(x)
                #             cur_rec = Currency.objects.get(name=xName)
                #             if cur_rec:
                #                 pass
                #             else:
                #                 Currency.objects.create(
                #                         name=xName,
                #                         code=xCode,
                #                         symbol=xSym
                #                     )
                #     except Exception as e:
                #         print(e)
                      
                # if file == "new_countries.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         native_name = data.get('Native_Name')
                #         country = data.get('Country')
                #         telephone_code = data.get("Telephone_Code")
                #         currency = data.get('Currency')
                #         symbol_position = data.get("Currency_Symbol_Position","")
                #         money_format = data.get('Money_Format',"")
                #         date_format = data.get("Date_Format","")
                #         time_format = data.get("Time_Format","")
                #         conList = list(native_name.keys())
                #         for x in conList:
                #             nName = native_name.get(x)
                #             cCon=country.get(x)
                #             xtel= telephone_code.get(x)
                #             xCurr = currency.get(x)
                #             sym = symbol_position.get(x)
                #             Mon= money_format.get(x)
                #             Date = date_format.get(x)
                #             Time = time_format.get(x)
                #             gcCur = Currency.objects.get_or_create(name=xCurr)
                #             sCur = Currency.objects.filter(name=xCurr).first()
                #             gcSym =Selectors.objects.get_or_create(selector =sym)
                #             sSym = Choice.objects.filter(choice_name=sym).first()
                #             gcMon =Selectors.objects.get_or_create(selector=Mon)
                #             sMon = Choice.objects.filter(choice_name=Mon).first()
                #             gcDate=Selectors.objects.get_or_create(selector=Date)
                #             sDate = Choice.objects.filter(choice_name=Date).first()
                #             gcTime =Selectors.objects.get_or_create(selector=Time)
                #             sTime = Choice.objects.filter(choice_name=Time).first()
                #             con_rec = Country.objects.filter(country = cCon)
                #             if con_rec:
                #                 pass
                #             else:
                                
                #                 Country.objects.create(
                #                         native_name=nName,
                #                         telephone_code=xtel,
                #                         country = cCon,
                #                         currency=sCur,
                #                         symbol_position=sSym,
                #                         money_format=sMon,
                #                         date_format=sDate,
                #                         time_format = sTime
                #                     )
                #     except Exception as e:
                #         print(e)
                        
                # if file == "new_states.xlsx":
                #     try:
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         country = data.get('Country')
                #         name = data.get('Name')
                #         seq = data.get("Sequence")
                #         sList = list(country.keys())
                #         for x in sList:
                #             con = country.get(x)
                #             gcCon = Country.objects.get_or_create(country=con)
                #             sCon = Country.objects.filter(country=con).first()
                #             sequence = seq.get(x)
                #             state_rec = State.objects.get(name= name)
                #             State.objects.create(
                #                     country=sCon,
                #                     name=name.get(x),
                #                 )
                #     except Exception as e:
                #         print(e)
                        
                
                        
                # if file == "Language.xlsx":
                #     try:
                    
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         name = data.get('English Name')
                #         native_Translation = data.get('Native Translation')
                #         code = data.get("Code")
                #         direction = data.get("Direction")
                #         dir_choice = data.get("Direction Choice ID")
                #         langList = list(native_Translation.keys())
                #         for x in langList:
                #             xName = name.get(x)
                #             nTrans = native_Translation.get(x)
                #             cod = code.get(x)
                #             dir = direction.get(x)
                #             dChoice = dir_choice.get(x)
                #             gcCon = Choice.objects.get_or_create(choice_name=dChoice)
                #             sCon = Choice.objects.filter(choice_name=dChoice).first()
                #             lang_rec =Language.objects.filter(name=xName)
                #             if lang_rec:
                #                 pass
                #             else:
                #                 Language.objects.create(
                #                         name=xName,
                #                         native_Translation = nTrans,
                #                         code = cod,
                #                         direction = dir,
                #                         dir_choice =sCon
                                        
                #                     )
                #     except Exception as e:
                #         print(e)
                        
                
                        
                # if file == "new_list.xlsx":
                #         data = pd.read_excel(os.path.join(folder,file)).to_dict()
                #         system_name = data.get('System_Name')
                #         category = data.get('Category')
                #         primary_table = data.get("Primary_Table")
                #         label = data.get('Label (US English)')
                #         list_type = data.get('List_Type')
                #         lList = list(system_name.keys())
                #         for x in lList:
                #             lName = system_name.get(x)
                #             ptable = primary_table.get(x)
                #             ltype = list_type.get(x)
                #             gcptble = Table.objects.get_or_create(table=ptable)
                #             sptble = Table.objects.filter(table=ptable).first()
                #             gcltp = Selectors.objects.get_or_create(selector=ltype)
                #             sltp = Choice.objects.filter(choice_name=ltype).first()
                #             list_rec = List.objects.get( system_name=lName)
                #             if list_rec:
                #                 pass
                #             else:
                                
                #                 List.objects.create(
                #                         system_name=lName,
                #                         primary_table=sptble,
                #                         list_type =sltp,
                                        
                #                     )
                        
                """if file == "MenuItemsFeb12.xlsx":
                    try:
                        data = pd.read_excel(os.path.join(folder,file)).to_dict()
                        name = data.get("System Name")
                        category_choice = data.get('Category')
                        description = data.get("System Description")
                        seq = data.get('Sequence')
                        lists = data.get('List')
                        visibility = data.get('Visibility')
                        lList = list(name.keys())
                        for x in lList:
                            mName = name.get(x)
                            cCat =category_choice.get(x)
                            desc=description.get(x)
                            sequence = int(seq.get(x))
                            vis = visibility.get(x)
                            l = lists.get(x)
                            print(l)
                            gccCat = Choice.objects.get_or_create(choice_name=cCat)
                            sCat = Choice.objects.filter(choice_name=cCat).first()
                            gclist = List.objects.get_or_create(system_name= l,primary_table=l)
                            sclist= List.objects.filter(system_name=l,primary_table=l).first()
                            gcvis = Selectors.objects.get_or_create(selector=vis)
                            svis = Choice.objects.filter(choice_name=vis).first()
                            menu_rec = Menu.objects.get(name=mName)
                            if menu_rec:
                                pass
                            else:
                                
                                Menu.objects.create(
                                            l = sclist,
                                            name=mName,
                                            category_choice=sCat,
                                            visibility=svis,
                                            description= desc,
                                            sequence = sequence
                                        )
                    except Exception as e:
                        print(e)
                        """
                        
            
                if file == "ColumnsFeb12.xlsx":
                        data = pd.read_excel(os.path.join(folder,file)).to_dict()
                        list = data.get('List')
                        column = data.get('System Name')
                        seq = data.get("Sequence")
                        dataset=data.get('Dataset')
                        data = data.get('Data System Name')
                        visibility = data.get('Visibility')
                        print(visibility)
                        slist = list(column.keys())
                        for x in slist:
                            clist = clist.get(x)
                            col = column.get(x)
                            dataset = dataset.get(x)
                            #sequence = int(seq.get(x))
                            data = data.get(x)
                            vis = visibility.get(x)
                            gclist = List.objects.get_or_create(system_name=clist)
                            slist = List.objects.filter(system_name=clist).first()
                            gcdatas = Dataset.objects.get_or_create(name=dataset)
                            sdatas = Dataset.objects.filter(name=dataset).first()
                            gcdata = Data.objects.get_or_create(name=data)
                            sdata = Data.objects.filter(name=data).first()
                            gcvis = Selectors.objects.get_or_create(selector=vis)
                            svis = Choice.objects.filter(choice_name=vis).first()
                            Column.objects.create(
                                    column=col,
                                    dataset=sdatas,
                                    data = sdata,
                                    #sequence =sequence,
                                    visibility=svis,
                                    clist = slist
                                    
                                )
                    
                
                