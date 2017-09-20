from __future__ import unicode_literals
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator
from django.db import models

from .base import *

class Payee(models.Model):
	customer = models.OneToOneField(Customer, null=True)#can choose to save payment details to customer profile
	stripe_customer_id = models.CharField(max_length=150)

class Payment(models.Model):
	cart = models.ForeignKey(Cart)
	amount = models.DecimalField(decimal_places=2,max_digits=100,blank=True)
	payee = models.ForeignKey(Payee)

class Refund(models.Model):
	amount = models.DecimalField(decimal_places=2,max_digits=100,blank=True)
	payment = models.ForeignKey(Payment)

class Cash_Payment(Payment):
	guide = models.ForeignKey(guide_models.Guide)
class Cash_Refund(Payment):
	guide = models.ForeignKey(guide_models.Guide)
class Stripe_Payment(Payment):
	stripe_charge_id = models.CharField(max_length=150)
class Stripe_Refund(Payment):
	stripe_refund_id = models.CharField(max_length=150)
