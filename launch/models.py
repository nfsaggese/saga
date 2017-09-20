from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Base_Model(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
         abstract=True #makes model abstract

class Guide(Base_Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    website = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
    sub_updates = models.BooleanField(default=True)
    sub_launch = models.BooleanField(default=False)

class Contact(Base_Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list