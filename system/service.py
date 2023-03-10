from system.models.recordid import RecordIdentifiers

def get_related_pkey(sender,initial,sequence):
    new_id=(int(initial)*1000)+int(sequence)
    record_id = RecordIdentifiers.objects.get(record=sender)
    record_id.next = new_id+1
    record_id.save()
    return new_id

def get_rid_pkey(sender):
    new_id = None
    record_id = RecordIdentifiers.objects.get(record=sender)
    code = record_id.code
    new_id = record_id.next
    if not new_id:
        start_id = record_id.starting
        new_id=start_id+1
    if code:
        primary_id = f'{code}{new_id}'
    else:
        primary_id = f'{new_id}'
    next_id=new_id+1
    record_id.next=next_id
    record_id.save()
    return primary_id

def updatenextid(sender, pid):
    record_id = RecordIdentifiers.objects.get(record=sender)
    record_id.next = int(pid)+1
    record_id.save()
    return None
# @receiver(post_save)
# def update_record_identifier(sender, created, **kwargs):
#     if created==True:
#         model_name = str(sender._meta)
#         text_split = model_name.split('.')
#         model_name=text_split[1]
#         record_id = RecordIdentifiers.objects.filter(record=model_name)
#         if record_id:
#             next_id = record_id.values()[0]['next']
#             new_id = next_id + 1
#             record_id.update(next=new_id)
#     return None