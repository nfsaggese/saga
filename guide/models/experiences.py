from __future__ import unicode_literals

from django.db import models
from scheduling import models as scheduling_models
from .standard import *
from photos import models as photos_models

class Hierarchy(models.Model):
	parent=models.ForeignKey('self',null=True)#subtype enablement
	name=models.CharField(max_length=50)
	description=models.TextField()

	class Meta:
		abstract = True

#CUSTOM Experience Definitions
#spec out but categorize: experiences, resources
#choose: fish species, location

#GUIDE SPECIFY
class Resource_Type(Hierarchy):
	pass
class Experience_Type(Hierarchy):
	pass

class Resource(models.Model): #equipment, gear used in an experience or multiple, has its own calendar
	published = models.BooleanField(default=False)
	resource_type = models.ForeignKey(Resource_Type)
	location = models.ManyToManyField(Location)
	turnover_time = models.DurationField()#how long till you can rent again, this includes times outside of the retnal return window
	transit_time = models.DurationField()#how long till can be used at a different location
	name = models.CharField(max_length=150)
	description = models.TextField()
	gallery = models.ForeignKey(photos_models.Gallery)
	perishable = models.BooleanField(default=False)#ie its a map, one use
	size_chart = models.ForeignKey(photos_models.Photo)

class Ind_Resource(scheduling_models.Actor):#individual iteration of a resource type...differs by size, id from umbrella resource type
	resource = models.ForeignKey(Resource)
	item_id = models.CharField(max_length=150, null=True)#this is for their curom definition...and search...we also use our id system..this overrides
	size = models.CharField(max_length=20)
	quantity = models.IntegerField(default=1)#for low value bulk reusables

class Guide_Equip_Preference(models.Model):
	guide = models.ForeignKey(Guide)
	resource = models.OneToOneField(Resource)
	pool = models.ManyToManyField(Ind_Resource)

class Experience(models.Model):
	# business = models.ForeignKey(Business, on_delete=models.CASCADE)
	location = models.ForeignKey('Location', on_delete=models.CASCADE)
	experience_type = models.ManyToManyField(Experience_Type,blank=True)#more than one of these could apply combo fishing/scuba
	max_capacity = models.IntegerField(default=0)#define how many can go, set 0 for unlimited, used for non tracked resource limits
	min_capacity = models.IntegerField(default=1)
	max_paralell = models.IntegerField(default=-1)#-1 unlimited, 0 none and so on
	meeting_address = models.ForeignKey(Address,blank=True)#pull from other experiences by the same biz
	description = models.TextField()
	waiver = models.ForeignKey(Waiver,null=True)
	product_type = models.CharField(max_length=150)#tour(g+r,s), course(g+r,s), rental(r,t), lesson(g+r,t)
	things_we_provide = models.TextField()#csl
	things_to_bring = models.TextField()#csl
	participant_reqs = models.TextField()
	gallery = models.ForeignKey(photos_models.Gallery)
	published = models.BooleanField(default=False)
class Tour(Experience):
	duration = models.DurationField()
class Course(Experience):
	duration = models.DurationField()
class Rental(Experience):
	pass
class Appointment(Experience):
	turnover_time = models.DurationField()
class Experience_Settings_Override(Setting):
	experience = models.OneToOneField(Experience)

class Schedule(models.Model):#status is by default going to be available
	experience = models.ForeignKey(Experience)
	event = models.ForeignKey(scheduling_models.Event)
	available = models.BooleanField(default=True)#use to set overrides on business hours
class Session(models.Model):
	experience = models.ForeignKey(Experience)
	session = models.ManyToManyField(scheduling_models.Event)
