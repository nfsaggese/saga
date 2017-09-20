from __future__ import unicode_literals

from django.db import models
from scheduling import models as scheduling_models
from .standard import *
from .experiences import *

class Requirement(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField(null=True)
	experience = models.ManyToManyField(Experience)#can use requirements repeatedly for syncing
	# pool = models.ManyToManyField(Resource)#implemented individually
	quantity_required = models.IntegerField()
	person_ratio = models.IntegerField()#how many people per piece
	customer_unique = models.BooleanField(default=False)#chosen 1/customer group
	guide_requirement = models.BooleanField(default=False)
	guide_shares = models.BooleanField(default=False)

class Resource_Pool(models.Model):
	requirement = models.ForeignKey(Requirement)
	quantity_required = models.IntegerField(null=True)#optional override
	person_ratio = models.IntegerField(null=True)#how many people per piece
	class Meta:
		abstract = True

class Guide_Body_Requirement(Requirement):
	pass
class Guide_Pool_Member(models.Model):
	requirement = models.ForeignKey(Guide_Body_Requirement)
	guide = models.ForeignKey(Guide)
	experience_level = models.IntegerField(default=50)#1-100
class Standard_Resource_Requirement(Requirement):
	pass
class Standard_Resource_Pool(Resource_Pool):
	pool = models.ManyToManyField(Resource)
class Standard_Specific_Resource_Requirement(Requirement):
	pass
class Standard_Specific_Resource_Pool(Resource_Pool):
	pool = models.ManyToManyField(Ind_Resource)

class Choice_Resource_Requirement(Requirement):#guides can't have choices
	optional = models.BooleanField(default=False)
	guide_requirement = False#may not need@-- guides can't have choices, fucks with checks for availability
	customer_unique = True
class Choice_Pool(Resource_Pool):
	# resource_choice_requirement = models.ForeignKey(Choice_Resource_Requirement)
	# default = models.BooleanField(default=False)
	hourly_price = models.BooleanField(default=False)
	price_adjustment = models.DecimalField(decimal_places=2,max_digits=100)

class Resource_Choice_Pool(Choice_Pool):
	pool = models.ManyToManyField(Resource)

class Specific_Resource_Choice_Pool(Choice_Pool):
	pool = models.ManyToManyField(Ind_Resource)
