from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *
#Guide Notes on Customers
class Note(models.Model):
	line_item = models.ForeignKey(Line_Item)
	body = models.TextField()
	class Meta:
		abstract=True
class Customer_Note(Note):
	by = models.ForeignKey(guide_models.Guide)
class Guide_Note(Note):
	by = models.ForeignKey(Customer)
