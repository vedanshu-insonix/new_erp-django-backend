from django.db import models
from .common import BaseContent

class Translation(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    label = models.CharField(max_length = 255, null=True, blank = True)
    description = models.CharField(max_length = 255, null=True, blank = True)
    default_label = models.CharField(max_length = 255, null=True, blank = True)
    default_description = models.CharField(max_length = 255, null=True, blank = True)
    language = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True, blank = True)
    table = models.ForeignKey('DataTable', on_delete = models.SET_NULL, null = True, blank = True)
    table_record = models.IntegerField(null=True, blank = True)
    
    # def __str__(self):
    #     return self.label 
class TranslationSelector(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    selector = models.ForeignKey('Selectors', on_delete = models.SET_NULL, null = True)
    
# class TranslationTable(BaseContent):
#     translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
#     table = models.ForeignKey('Table', on_delete = models.SET_NULL, null = True)
    
class TranslationData(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    name = models.ForeignKey('Data', on_delete = models.SET_NULL, null = True)

class TranslationIcons(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    icon = models.ForeignKey('Icons', on_delete = models.SET_NULL, null = True)
    
class TranslationCurrency(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    currency = models.ForeignKey('Currency', on_delete = models.SET_NULL, null = True)
    
class TranslationConfiguration(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    Configuration = models.ForeignKey('Configuration', on_delete = models.SET_NULL, null = True)
    
# class TranslationState(BaseContent):
#     translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
#     state = models.ForeignKey('State', on_delete = models.SET_NULL, null = True)
    
# class TranslationEntity(BaseContent):
#     translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
#     entity = models.ForeignKey('Entity', on_delete = models.SET_NULL, null = True)
    
class TranslationContainerType(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.SET_NULL, null = True)
    containerType = models.ForeignKey('warehouse.ContainerTypes', on_delete = models.SET_NULL, null = True)
    
class TranslationColumn(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    column = models.ForeignKey('Column', on_delete = models.CASCADE, null = True)
    
class TranslationFromData(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    formdata = models.ForeignKey('FormData', on_delete = models.CASCADE, null = True)
    
class TranslationMenu(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    menu = models.ForeignKey('Menu', on_delete = models.CASCADE, null = True)
    
class TranslationChoice(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    choice = models.OneToOneField('Choice', on_delete=models.CASCADE, null = True)
    
class TranslationHelp(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    help = models.ForeignKey('Help', on_delete=models.CASCADE, null = True)
    
class TranslationButton(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    button = models.ForeignKey('Button', on_delete=models.CASCADE, null = True)
    
class TranslationStage(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, null = True)
    
class TranslationTag(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null = True)
    
class TranslationTile(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    tag = models.ForeignKey('Tile', on_delete=models.CASCADE, null = True)
    
class TranslationList(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    list = models.OneToOneField('List', on_delete=models.CASCADE, null = True)

class TranslationForm(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    form = models.ForeignKey('Form', on_delete=models.CASCADE, null = True)
    
class TranslationStageAction(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    stage_action = models.ForeignKey('StageAction', on_delete=models.CASCADE, null = True)

class TranslationFormSection(BaseContent):
    translation = models.OneToOneField('Translation', on_delete=models.CASCADE, null = True)
    form = models.ForeignKey('FormSection', on_delete=models.CASCADE, null = True)