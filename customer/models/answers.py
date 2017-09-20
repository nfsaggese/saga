from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *
#Q+A answers
class Choice(models.Model):
	choice = models.ForeignKey(guide_models.Answer_Choice)
	class Meta:
		abstract = True
class Answer(models.Model):
	question = models.ForeignKey(guide_models.Question)
	answer = models.TextField()
	class Meta:
		abstract = True

class Customer_Choice(Choice):#group question
 	choice = models.ForeignKey(guide_models.Experience_Answer_Choice)
	customer = models.ForeignKey(Customer)

class Party_Member_Choice(Choice):
	choice = models.ForeignKey(guide_models.Experience_Answer_Choice)
	party_member = models.ForeignKey(Party_Member)

class Customer_Answer(Answer):
	question = models.ForeignKey(guide_models.Experience_Question)
	customer = models.ForeignKey(Customer)

class Party_Member_Answer(Answer):
	question = models.ForeignKey(guide_models.Experience_Question)
	party_member = models.ForeignKey(Party_Member)
