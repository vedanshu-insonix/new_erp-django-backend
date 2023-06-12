# Manual Pkey generation feature.
from system.models.recordid import RecordIdentifiers

# used to generate pkey in child models.(eg:- choices, states)
def get_related_pkey(sender,initial,sequence):
    new_id=(int(initial)*1000)+int(sequence)
    record_id = RecordIdentifiers.objects.get(record=sender)
    record_id.next = new_id+1
    record_id.save()
    return new_id

# used to generate pkey in parent models.(eg:- selectors, country)
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
    if sender == 'datatable':
        next_id=new_id+10
    else:
        next_id=new_id+1
    record_id.next=next_id
    record_id.save()
    return primary_id

# used to update next pkey for a model in recordidentifier model.(Note:- Currently used in custom_command only.)
def updatenextid(sender, pid):
    record_id = RecordIdentifiers.objects.get(record=sender)
    if sender == 'datatable':
        record_id.next = int(pid)+10
    else:
        record_id.next = int(pid)+1
    record_id.save()
    return None