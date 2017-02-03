from oscar.apps.customer.models import Email
from oscar.apps.address.models import Country
from oscarapps.address.models import States,Locations
import datetime




def SaveSendMail(userObj,Sub,Body):
    try :
        now = datetime.datetime.now()
        recordEmail = Email.objects.create(user=userObj,
                                         subject=Sub,
                                         body_html=Body ,
                                         date_sent=str(now.strftime("%Y-%m-%d_%H:%M:%S.%f"))
                                         )
        recordEmail.save()
    except :
        pass


