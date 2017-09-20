from rest_framework import serializers
from . import models

class Guide_Serializer(serializers.ModelSerializer):
	class Meta:
		model = models.Guide
		fields = '__all__'

class Contact_Serializer(serializers.ModelSerializer):
	class Meta:
		model = models.Contact
		fields = '__all__'
