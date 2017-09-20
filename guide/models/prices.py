from __future__ import unicode_literals

from django.db import models
from scheduling import models as scheduling_models
from .experiences import *

class Price_Demographic(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	min_age = models.IntegerField()
	max_age = models.IntegerField()

class Price(models.Model):#per person
	experience = models.ForeignKey(Experience)
	demo = models.ManyToManyField(Price_Demographic)# can have multiple demos
	name = models.CharField(max_length=100)
	desc = models.TextField()
	price = models.DecimalField(decimal_places=2,max_digits=100)
	date_void = models.DateTimeField(null=True)
	capacity = models.IntegerField()#1 seat? 2 seats? the whole thing? let us know!
	private = models.BooleanField(default=False)#sets min capacity to doesn't matter
	standard = models.BooleanField(default=True)#always used


class Time_Price(Price):
	min_duration = models.DurationField()#half hour, two hours, 4 hours, 1 day etc.
	max_duration = models.DurationField()#TODO handle check in time
	hourly_price = models.BooleanField(default=False)
	private = True
	schedule = models.ManyToManyField(Schedule)

class Event_Price(Price):
	schedule = models.ManyToManyField(Schedule)
	#if set true it make the ticket one that if sold doesn't allow any other tickets, not sure if its necessary

class Session_Price(Price):
	num_events = models.IntegerField(default=0)#0 is same as all
	session = models.ManyToManyField(Session)

class Class_Pack(Price):
	num_events = models.IntegerField(default=1)
	expiration = models.DurationField()
#class Membership()

class Standard_Price_Exclusions(Price):
	session = models.ManyToManyField(Session)
	schedule = models.ManyToManyField(Schedule)
