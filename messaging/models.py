from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from shifts import models as shift_models
from customer import models as customer_models
from guide import models as guide_models
# Create your models here.
class Message(models.Model):
	recipient = models.ManyToManyField(User, related_name="recipient")
	sender = models.ForeignKey(User, related_name="sender")
	body = models.TextField()
	method = models.CharField(max_length=150)#sms,email
	class Meta:
		abstract = True
class Shift_Message(Message):
	sender = models.ForeignKey(guide_models.Guide)
	shift = models.ForeignKey(shift_models.Scheduled_Shift)
	recipient = models.ManyToManyField(guide_models.Guide, related_name='shift_recipient')
class Experience_Message(Message):
	sender = models.ForeignKey(guide_models.Guide)
	experience = models.ForeignKey(customer_models.Product_Experience)
	class Meta:
		abstract = True
class Guide_Guide_Message(Experience_Message):
	recipient = models.ManyToManyField(guide_models.Guide, related_name='recipient')
class Guide_Customer_Message(Experience_Message):
	recipient = models.ManyToManyField(customer_models.Customer)
class Guide_Party_Member_Message(Experience_Message):
	recipient = models.ManyToManyField(customer_models.Party_Member)
