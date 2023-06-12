from django.db import models
from .common import BaseContent

class DataTable(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    system_name = models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True, blank=True)
    link_source = models.CharField(max_length=255, null=True, blank=True)

class Data(BaseContent):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    data_source=models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_model')
    linked_ds = models.ForeignKey('DataTable', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_model')
    system_name= models.CharField(max_length=255, null=True, blank=True)
    linked_data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)
    data_type = models.CharField(max_length=255, null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True)
    # field_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    field_type = models.CharField(max_length=255, null=True, blank=True)
    selector = models.ManyToManyField('Selectors', blank=True, related_name='data')

# class DataSelector(BaseContent):
#     selector = models.ForeignKey('Selectors', on_delete=models.SET_NULL, null=True, blank=True)
#     data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)

class DataRequirements(BaseContent):
    form = models.ForeignKey('Form', on_delete=models.SET_NULL, null=True, blank=True)
    data = models.ForeignKey('Data', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True)
    requirement = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)

# class SchemaRelation(BaseContent):
#     primary = models.CharField(max_length=255, null=True, blank=True)
#     related = models.CharField(max_length=255, null=True, blank=True)
#     relation = models.CharField(max_length=255, null=True, blank=True)
#     primary_field = models.CharField(max_length=255, null=True, blank=True)
#     related_field = models.CharField(max_length=255, null=True, blank=True)
#     primay_rec = models.BooleanField(default=False)
#     primay_rec_field = models.CharField(max_length=255, null=True, blank=True)