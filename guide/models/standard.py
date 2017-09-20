from __future__ import unicode_literals

from django.db import models
from scheduling import models as scheduling_models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from photos import models as photo_models

import datetime
from datetime import timedelta
import pytz
from pytz import timezone

# from .experiences import *
class Setting(models.Model):
	no_rebook = models.BooleanField(default=False)
	rebook_cutoff = models.DurationField(default=timedelta(days=1))

	no_cancel = models.BooleanField(default=False)
	cancel_cutoff = models.DurationField(default=timedelta(days=3))

	no_customer_change = models.BooleanField(default=False)
	customer_change_cutoff = models.DurationField(default=timedelta(hours=3))#within this, no changes allowed w/o call...admin panel input
	online_sales_cutoff = models.DurationField(default=timedelta(hours=3))

	rebook_grace_period = models.DurationField(default=timedelta(days=1))#up to this point
	return_grace_period = models.DurationField(default=timedelta(hours=1))

	late_return_fee_percent = models.BooleanField(default=False)
	late_return_fee = models.DecimalField(decimal_places=5,max_digits=100,default=5.00)

	#automatically induces a refund
	cancel_fee_percent = models.BooleanField(default=True)
	cancel_fee = models.DecimalField(decimal_places=5,max_digits=100,default=0.5)

	reschedule_fee_percent = models.BooleanField(default=False)
	reschedule_fee = models.DecimalField(decimal_places=5,max_digits=100,default=0.00)

	rent_out_hours = models.BooleanField(default=True)#renting can continue outside of hours
	# rental_out_hours_pd = models.BooleanField(default=False)#renting can start or end outside of hours

	guide_cancellation_window = models.DurationField(default=timedelta(hours=12))

	auto_check_in_resources = models.BooleanField(default=True)
	auto_check_out_guides = models.BooleanField(default=True)

	deposit_percent = models.DecimalField(decimal_places=2,max_digits=100,default=1.00)#all deposit by default

	class Meta:
		abstract = True
# Create your models here.
class Business(Setting):
	plan = models.CharField(max_length=200, default="basic")#mid,elite
	name = models.CharField(max_length=150)
	#subdomain?
	logo = models.ForeignKey(photo_models.Photo, null=True)


class Location(models.Model):
	published = models.BooleanField(default=False)
	business = models.ForeignKey('Business', on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	tz = TimeZoneField(default='America/New_York')
	sales_tax_rate = models.DecimalField(decimal_places=5, max_digits=100,default=0)
	business_hours = models.ManyToManyField(scheduling_models.Event)
	email_address = models.EmailField(max_length=254)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
class Location_Setting(Setting):
	location = models.OneToOneField(Location)

class Guide(User):#person in the business, all get a login, notifications
	business = models.ForeignKey('Business', on_delete=models.CASCADE)
	roles = models.CharField(max_length=500)#CSV, admin, guide, employee, manager
	actor = models.OneToOneField(scheduling_models.Actor)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
	location = models.ManyToManyField(Location)
	#vacation time?
	# tags = models.CharField(max_length=250)#add employees by tag csv
class Suspended_Guide(scheduling_models.Suspended):
	guide = models.ForeignKey(Guide)

class Address(models.Model):
	number = models.CharField(max_length=30)
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=25)
	country = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=25)

class Meeting_Address(Address):
	name = models.CharField(max_length=150)
	location = models.ForeignKey('Location', on_delete=models.CASCADE)

class Cause(models.Model):#in order to see analysis on why events are most often changed and canceled
	name = models.CharField(max_length=150)
	desc = models.TextField()

class Waiver(models.Model):
	published = models.BooleanField(default=False)
	business = models.ForeignKey(Business, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	body = models.TextField()#change to text file url in s3 TODO
	# expiration = models.DurationField()#from point of signing
