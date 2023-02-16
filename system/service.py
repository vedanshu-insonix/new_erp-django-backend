from system.models.recordid import RecordIdentifiers
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_primary_key(sender):
    next_id = None
    record_id = RecordIdentifiers.objects.filter(record=sender)
    if record_id:
        code = record_id.values()[0]['code']
        next_id = record_id.values()[0]['next']
        if not next_id:
            start_id = record_id.values()[0]['starting']
            next_id=start_id+1
        primary_id = f'{code}{next_id}'
        return primary_id
    else:
        return None
    
# @receiver(post_save)
# def update_record_identifier(sender, created, instance, **kwargs):
#     if created==True:
#         model_name = str(sender._meta)
#         text_split = model_name.split('.')
#         model_name=text_split[1]
#         record_id = RecordIdentifiers.objects.filter(record=model_name.capitalize())
#         if record_id:
#             next_id = record_id.values()[0]['next']
#             new_id = next_id + 1
#             record_id.update(next=new_id)
#     return None