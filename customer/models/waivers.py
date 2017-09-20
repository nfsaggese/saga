from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *
from .answers import *
class Signature(models.Model):
	waiver = models.ForeignKey(guide_models.Waiver)
	signature = models.FileField()#some kind of url to s3 with png signature
	dateTime = models.DateTimeField(auto_now=True)#check this TODO
	signee = models.ForeignKey(Person)

class Guardian_Signature(models.Model):
	guardian_signature = models.ForeignKey(Signature)
	minor = models.ForeignKey(Person,related_name="minor")

class Waiver_Choice(Choice):
	signature = models.ForeignKey(Signature)
	choice = models.ForeignKey(guide_models.Waiver_Answer_Choice)

class Waiver_Answer(Answer):
	signature = models.ForeignKey(Signature)
	question = models.ForeignKey(guide_models.Waiver_Question)
