from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *
class Resource_Allocation(models.Model):
	line_item = models.ForeignKey(Line_Item)
	ind_resource = models.ForeignKey(guide_models.Ind_Resource)
	quantity = models.IntegerField()
	requirement = models.ForeignKey(guide_models.Requirement)

class Guide_Assignment(models.Model):
	line_item = models.ForeignKey(Line_Item)
	guide = models.ForeignKey(guide_models.Guide, related_name='assigned')
	requirement = models.ForeignKey(guide_models.Requirement)

class Resource_Choice(models.Model):#joins resource choices to the party member
	party_member = models.ForeignKey(Party_Member)
	line_item = models.ForeignKey(Line_Item)
	choice_pool = models.ForeignKey(guide_models.Choice_Pool)
	ind_resource = models.ForeignKey(guide_models.Ind_Resource)
	quantity = models.IntegerField()
	charge = models.DecimalField(decimal_places=2,max_digits=100)
