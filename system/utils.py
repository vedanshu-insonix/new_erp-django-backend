from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status

EntityChoice = (
    ("1", "Person"),
    ("2", "Company"),
)

ShippingTermsChoice = (
    ("1", "Prepaid/Prepay"),
    ("2", "Add/Collect"),
)

AddressTypeChoice=(
("1","Customer"),
("2","Billing"),
("3", "Shipping"),
)

LocationChoice=(
    ("1","Residential"),
    ("2","Commercial"),
    ("3","Construction Site")
)

ColumnTypeChoice=(
    ("1","string"),
    ("2","int"),
    ("3","boolean"),
    ("4","lookup"),
    ("5","date"),
    ("6", "datetime"),
    ("7", "multi-choice"),   
)

StatusChoice=(
    ("1","Closed"),
    ("2","Normal"),
    ("3","Warning"),
    ("3","Urgent"),
)

ChannelTypeChoice=(
    ("1","Home"),
    ("2","Work"),
    ("3", "Personal")
)

DateFormatChoices=(
    
    ("1", "MM/DD/YY"),
    ("2", "DD/MM/YY"),
    ("3", "YY/MM/DD"),
    ("4", "MM-DD-YYYY"),
    ("5", "DD-MM-YYYY"),
    ("6", "YYYY-MM-DD"),
)

TimeFormatChoice =(
    
    ("1","HH:MM:SS"),
    ("2","HH:MM:SS XM"),
    ("3","HH:MM"),
    ("4","HH:MM XM")
    
)

Column_Visibility_Choice =(
    ("1","Required"),
    ("2","Optional"),
    ("3","Default")
)
""" Send email function """
def send_email(subject, message, mail_to, mail_from=None, attachement=None):
    try:
        backend = EmailBackend(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, username=settings.EMAIL_HOST_USER, 
                            password=settings.EMAIL_HOST_PASSWORD, use_tls=settings.EMAIL_USE_TLS)
        
        if mail_from is None: mail_from = settings.EMAIL_HOST_USER
        sent = EmailMessage(subject, message, mail_from, [mail_to], connection=backend)
        if attachement: sent.attach_file(attachement)
        try : 
            status = sent.send()
            return status
        except Exception as err:
            raise ValueError(err)
    except Exception as err:
        raise ValueError(err)

## Uniform api response
def success(self, count):
    response = {
                    'inserted': str(count)+" row(s) inserted successfully",
                    "status" : "success",
                    "code"   : status.HTTP_200_OK
                }
    return response

def error(self, msg):
    response = {
                    "message": msg,
                    "status" : "error",
                    "code"   : status.HTTP_400_BAD_REQUEST
                }
    return response

def success_def(self,count,defective_data):
    response = {
                    'inserted': str(count)+" row(s) inserted successfully",
                    "status" : "success",
                    "rejected_records" : defective_data,
                    "code"   : status.HTTP_200_OK
                }
    return response

#*************** Encode API Name **************
def encode_api_name(value):
    lowercase = value.lower()
    value = lowercase.replace(" ", "_")
    return value

#*************** Decode API name ***************
def decode_api_name(value):
    captalize = value.title()
    value = captalize.replace("_", " ")
    return value
