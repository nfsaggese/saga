from __future__ import unicode_literals

from django.db import models
from guide import models as guide_models
from scheduling import models as scheduling_models
import datetime
from datetime import timedelta
# Create your models here.
class Role(models.Model):
	published = models.BooleanField(default=False)
	name = models.CharField(max_length=50)
	desc = models.TextField()
	location = models.ForeignKey(guide_models.Location, on_delete=models.CASCADE)
	#for reserve workers and experience scheduling
	can_schedule = models.BooleanField(default=True)
	scheduling_notice = models.DurationField(default=datetime.timedelta(minutes=30))
	#set available attribute based upon desire to double schedule this shift
class Shift_Worker(models.Model):
	shift = models.ForeignKey(Role)
	experience_level = models.IntegerField(default=50)#1-100 exp level
	guide = models.ForeignKey(guide_models.Guide)

class Resource_Requirement(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField(null=True)
	role = models.ManyToManyField(Role)#can use requirements repeatedly for syncing
	quantity_required = models.IntegerField()
	person_ratio = models.IntegerField()#how many people per piece


class Resource_Pool(models.Model):
	requirement = models.ForeignKey(Resource_Requirement)
	quantity_required = models.IntegerField(null=True)#optional override
	person_ratio = models.IntegerField(null=True)#how many people per piece
	class Meta:
		abstract = True
class Standard_Resource_Pool(Resource_Pool):
	pool = models.ManyToManyField(guide_models.Resource, related_name='resource')
class Specific_Resource_Pool(Resource_Pool):
	pool = models.ManyToManyField(guide_models.Ind_Resource, related_name='spec_resource')

class Scheduled_Shift(scheduling_models.Event):
	shift = models.ForeignKey(Role)
	workers = models.IntegerField(default=1)
	

class Guide_Assignment(models.Model):
    shift = models.ForeignKey(Scheduled_Shift)
    guide = models.ForeignKey(guide_models.Guide)

class Resource_Assignment(models.Model):
    qty = models.IntegerField(default=1)
    requirement = models.ForeignKey(Resource_Requirement)
    shift = models.ForeignKey(Scheduled_Shift)
    resource = models.ForeignKey(guide_models.Ind_Resource)
#switches here
