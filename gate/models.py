from __future__ import unicode_literals

from django.db import models

from guide import models as guide_models
from scheduling import models as scheduling_models
from customer import models as customer_models
from photos import models as photo_models
# Create your models here.
class Request_Time_Off(Unavailable):#TODO for people, look for series, move this....
	# reason = models.TextField()
	expiration = models.DateTimeField()
	request_by = models.ForeignKey(Guide)#if approved add this actor as attendee
	# approved = models.BooleanField(default=False)
class Time_Off_Decision(Request_Time_Off):
	dt = models.DateTimeField(auto_now=True)
	decision_by = models.ForeignKey(Guide)
	approved = models.BooleanField()

class Resource_Damaged(scheduling_models.Suspended):
	resource = models.ForeignKey(guide_models.Individual_Resource)
	damage = models.IntegerField()
	gallery = models.ForeignKey(photos_models.Gallery)

class Resource_Broken(scheduling_models.Terminated):
	resource = models.ForeignKey(guide_models.Individual_Resource)

#resource check in
class Resource_Check_In(scheduling_models.Check_In):
	resource = models.ForeignKey(guide_models.Individual_Resource)
#guide check in
class Guide_Check_In(scheduling_models.Check_In):
	guide = models.ForeignKey(guide_models.Guide)
#party_member check in
class Party_Member_Check_In(scheduling_models.Check_In):
	party_member = models.ForeignKey(customer_models.Party_Member)
#resource check out
class Resource_Check_Out(scheduling_models.Check_Out):
	resource = models.ForeignKey(guide_models.Individual_Resource)
#guide check out
class Guide_Check_Out(scheduling_models.Check_Out):
	guide = models.ForeignKey(guide_models.Guide)
#party_member check out
class Party_Member_Check_Out(scheduling_models.Check_Out):
	party_member = models.ForeignKey(customer_models.Party_Member)
#fired guide
class Guide_Fired(scheduling_models.Terminated):
	guide = models.ForeignKey(guide_models.Guide)

#suspended guide
class Guide_Suspended(scheduling_models.Suspended):
	guide = models.ForeignKey(guide_models.Guide)

#guide cancel
class Guide_Cancel(scheduling_models.Cancellation):
	guide = models.ForeignKey(guide_models.Guide)

#shift replacement request_by
class Guide_Switch_Request(models.Model):
	expiration = models.DateTimeField()
	event = models.ForeignKey(scheduling_models.Event)
	guide_out = models.ForeignKey(guide_models.Guide)
	replacements = models.ManyToManyField(guide_models.Guide)
	class Meta:
		abstract = True
class Guide_Shift_Switch_Request(Guide_Switch_Request):
	shift = models.ForeignKey(shift_models.Scheduled_Shift)
class Guide_Experience_Switch_Request(Guide_Switch_Request):
	experience = models.ForeignKey(guide_models.Experience)
	#get guide assignment no reference
class Guide_Switch_Denied(models.Model):
	request = models.ForeignKey(Guide_Switch_Request)
	denyee = models.ForeignKey(guide_models.Guide)

class Guide_Switch_Accept(models.Model):
	request = models.ForeignKey(Guide_Switch_Request)
	acceptee = models.ForeignKey(guide_models.Guide)
	time_block = models.ForeignKey(scheduling_models.Unavailable)#for the old guide
#experience replacement request
