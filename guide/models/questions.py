from __future__ import unicode_literals

from django.db import models
from scheduling import models as scheduling_models
from .experiences import *

class Question(models.Model):
	question = models.CharField(max_length=250)
	class Meta:
		abstract = True
class Experience_Question(Question):#lunch options
	experience = models.ForeignKey(Experience)
	group_question = models.BooleanField(default=True)
	every_participant = models.BooleanField(default=False)
class Waiver_Question(Question):
	waiver = models.ForeignKey(Waiver)
    
class Answer_Choice(models.Model):
	question = models.ForeignKey(Question)#can i access? TODO
	text = models.CharField(max_length=250)
	class Meta:
		abstract = True

# add on questions
class Waiver_Answer_Choice(Answer_Choice):
	question = models.ForeignKey(Waiver_Question)

class Experience_Answer_Choice(Answer_Choice):
	question = models.ForeignKey(Experience_Question)
	hourly_adjustment = models.BooleanField(default=False)#False is its a fixed price adjustment
	price_adjustment = models.DecimalField(decimal_places=2,max_digits=100)
