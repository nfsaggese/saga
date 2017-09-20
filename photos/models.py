from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Gallery(models.Model):
    pass

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    #s3 link
