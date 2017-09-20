from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from scheduling import models as scheduling_models
from guide import models as guide_models
from django.core.validators import RegexValidator

class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
    dob = models.DateField(null=True)
    address = models.ForeignKey(guide_models.Address, null=True)#street address

# Create your models here.
class Customer(Person):
	user = models.OneToOneField(User)
	actor = models.OneToOneField(scheduling_models.Actor)

class Cart(models.Model):
	customer = models.ForeignKey(Customer)

class Hold(models.Model):
    cart = models.ForeignKey(Cart)
    end = models.DateTimeField()
    by = models.ForeignKey(guide_models.Guide,null=True)#null in case where for checkout purposes

class Share(Hold):
    person = models.ForeignKey(Person)

class Line_Item(models.Model):
	cart = models.ForeignKey(Cart)
	total_price = models.DecimalField(decimal_places=2,max_digits=100)

class Product_Experience(Line_Item):
	num_attendees = models.IntegerField()
	experience = models.ForeignKey(guide_models.Experience)
	event = models.ManyToManyField(scheduling_models.Event)

class Party_Member(Person):
	cart = models.ForeignKey(Cart)

class Pricepoint(models.Model):
	item = models.ForeignKey(Line_Item)
	price = models.ForeignKey(guide_models.Price)
	quantity = models.IntegerField()
