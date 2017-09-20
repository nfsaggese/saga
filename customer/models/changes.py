from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *
#changes
class Change(models.Model):
	cause = models.ForeignKey(guide_models.Cause)
	desc = models.TextField(blank=True)
	fee = models.DecimalField(decimal_places=2,max_digits=100)
	class Meta:
		abstract=True

class Cancellation(Change):#is final
	item = models.OneToOneField(Line_Item)

class Rebook(Change):#occurs independently of cancellation, any time there is a date change
	old_item = models.OneToOneField(Line_Item, related_name='old')
	new_item = models.OneToOneField(Line_Item, related_name='new')

class Group_Resource_Addition(models.Model):
	line_item = models.ForeignKey(Line_Item)
	ind_resource = models.ForeignKey(guide_models.Ind_Resource)
	quantity = models.IntegerField()
class Guide_Resource_Addition(models.Model):
	line_item = models.ForeignKey(Line_Item)
	ind_resource = models.ForeignKey(guide_models.Ind_Resource)
	quantity = models.IntegerField()
