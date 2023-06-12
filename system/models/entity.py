from django.db import models
from system.models.common import BaseContent, BaseStatus
from django.contrib.auth.models import User

class Entity(BaseStatus):
    id = models.CharField(max_length=255, primary_key=True, editable=False)
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null=True, blank=True)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    entity_type = models.ForeignKey('Choice', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ManyToManyField(User, blank=True, related_name='entity')
    product = models.ManyToManyField('warehouse.Product', blank=True, related_name='entity')
    team = models.ManyToManyField('Team', blank=True, related_name='entity')
    account = models.ManyToManyField('warehouse.Accounts', blank=True, related_name='entity')
    form = models.ManyToManyField('Form', blank=True, related_name='entity')
    list = models.ManyToManyField('List', blank=True, related_name='entity')
    menu = models.ManyToManyField('Menu', blank=True, related_name='entity')
    
    def __str__(self):
        return self.system_name
    
    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
    

# class EntityUser(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
#     def __str__(self):
#         return self.user
    
# class EntityAddress(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True)
#     address = models.ForeignKey(Addresses, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return self.address
    
# class EntityProducts(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey('warehouse.Product', on_delete=models.CASCADE, null=True, blank=True)

# class EntityTeam(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)

# class EntityAccounts(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     accounts = models.ForeignKey('warehouse.Accounts', on_delete=models.CASCADE, null=True, blank=True)

# class EntityForms(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     form = models.ForeignKey('Form', on_delete=models.CASCADE, null=True, blank=True)

# class EntityList(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     list = models.ForeignKey('List', on_delete=models.CASCADE, null=True, blank=True)

# class EntityMenuItem(BaseContent):
#     entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True)
#     menu_item = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, blank=True)