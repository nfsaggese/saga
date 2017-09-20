from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *

class Discount_Code(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	percentage = models.DecimalField(decimal_places=2,max_digits=100,blank=True)
	amount = models.DecimalField(decimal_places=2,max_digits=100, blank=True)
	items = models.ManyToManyField(guide_models.Experience,blank=True)#applicable items for discount, blank for all

class Applied_Discount(models.Model):
	cart = models.ForeignKey(Cart)

class Manual_Discount(Applied_Discount):
	guide = models.ForeignKey(guide_models.Guide, blank=True)#manual discount
	amount = models.DecimalField(decimal_places=2,max_digits=100, blank=True)
	percentage = models.DecimalField(decimal_places=2,max_digits=100, blank=True)

class Automatic_Discount(Applied_Discount):
	code = models.ForeignKey(Discount_Code, blank=True)#if manually applied
