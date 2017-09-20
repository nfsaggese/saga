import django
django.setup()

import datetime
from datetime import timedelta
import pytz
from pytz import timezone

from guide import models

eficax = models.Business(name="Eficax Coaching",no_rebook_window=timedelta(days=1),no_cancel_window=timedelta(days=3),return_grace_period=timedelta(hours=1))
eficax.save()

from scheduling import models as scheduling_models
act = scheduling_models.Actor()
act.save()
nick = models.Guide(actor=act,business=eficax,username="nick",first_name="nick",last_name="saggese",email="nicholas@eficaxstudios.com",password="password",phone_number=3172097889,tags="coach,",roles="admin")
nick.save()

home = models.Address(business=eficax,nickname="Home",address="1192 N. Claridge Way",city="Carmel",state="Indiana",zip_code="46032")
home.save()

onetoone = models.Experience(business=eficax,meeting_address=home,description="1 on 1 coaching session.",)
onetoone.save()

req = models.Guide_Requirement(name="Sample",experience=onetoone,quantity_required=1,person_ratio=1)
req.save()
req.pool.add(nick)

eastern = timezone('US/Eastern')
#year, month, day
start = datetime.datetime(2017,12,3, tzinfo=eastern)
event1 = scheduling_models.Event(
    start=start,
    end=(start+datetime.timedelta(hours=8)),
    available = False
)
event1.save()

scheduling_models.Attendee(event=event1,actor=nick.actor).save()

start = datetime.datetime(2017,12,5, tzinfo=eastern)
event2 = scheduling_models.Event(
    start=start,
    end=(start+datetime.timedelta(hours=8)),
    available = False
)
event2.save()
scheduling_models.Attendee(event=event2,actor=nick.actor).save()

#look at 12/1-12/7/17
#timezone not active...
