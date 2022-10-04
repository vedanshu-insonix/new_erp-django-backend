from lib2to3.pytree import Base
from django.db import models
from .common import BaseContent

class Translation(BaseContent):
    type = models.CharField(max_length = 255, null=True, blank = True)
    item = models.CharField(max_length = 255, null=True, blank = True)
    label = models.CharField(max_length = 255, null=True, blank = True)
    sub_label = models.CharField(max_length = 255, null=True, blank = True)
    language = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True, blank = True)
    translation = models.CharField(max_length = 255, null=True, blank = True)
    
    
class TranslationColumn(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    column = models.ForeignKey('Columns', on_delete = models.CASCADE, null = True)
    
class TranslationFromData(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    formdata = models.ForeignKey('FormData', on_delete = models.CASCADE, null = True)
    
class TranslationMenu(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    menu = models.ForeignKey('Menu', on_delete = models.CASCADE, null = True)
    
class TranslationChoice(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE, null = True)
    
class TranslationHelp(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    help = models.ForeignKey('Help', on_delete=models.CASCADE, null = True)
    
class TranslationButton(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    button = models.ForeignKey('Button', on_delete=models.CASCADE, null = True)
    
class TranslationStage(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, null = True)
    
class TranslationTag(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null = True)
    
class TranslationTile(BaseContent):
    translation = models.ForeignKey('Translation', on_delete=models.CASCADE, null = True)
    tag = models.ForeignKey('Tile', on_delete=models.CASCADE, null = True)

