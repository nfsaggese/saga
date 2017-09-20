from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Series(models.Model):#binds recurring events
	ruleString = models.CharField(max_length=300)

class Actor(models.Model):
	pass

class Event(models.Model): #when someone applies a block of time they don't want to work?
 	start = models.DateTimeField()
	end = models.DateTimeField()
	series = models.ForeignKey(Series, null=True)
	series_base = models.BooleanField(default=False)
	available = models.BooleanField(default=True)

class Attendee(models.Model):
	event = models.ForeignKey(Event)
	quantity = models.IntegerField(default=1) #only relevant for resources where multi needed
	actor = models.ForeignKey(Actor)

class Unavailable(Event):#used on equipment
	reason = models.TextField()
	approved = True
	available = False
	
# class Hold(Event):
# 	end_hold = models.DateTimeField()#when does this hold expire? we can eliminate these holds periodically? or likely build in logic into checking mechanisms
class Suspended(models.Model):#broken, off season
	start = models.DateTimeField(auto_now=True)
	end = models.DateTimeField(null=True)
	actor = models.ForeignKey(Actor)
	qty = models.IntegerField(default=1)
	desc = models.TextField(null=True)

class Terminated(Actor):#destroyed, fired, etc
	dt = models.DateTimeField(auto_now=True)
	qty = models.IntegerField(default=1)
	desc = models.TextField(null=True)

# class Present(models.Model):#people
# 	event = models.ForeignKey(Event)
# 	actor = models.ForeignKey(Actor)
# 	time = models.DateTimeField(auto_now=True)

class Check_Out(models.Model):#things
	event = models.ForeignKey(Event)
	actor = models.ForeignKey(Actor)
	time = models.DateTimeField(auto_now=True)

class Check_In(models.Model):
	event = models.ForeignKey(Event)
	actor = models.ForeignKey(Actor)
	time = models.DateTimeField(auto_now=True)

class Cancellation(models.Model):#last min issue with showing up...system can try and fix it
	dt = models.DateTimeField(auto_now=True)
	event = models.ForeignKey(Event)
	by = models.ForeignKey(Actor)#person dropping out
