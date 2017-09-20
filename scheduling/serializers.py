from rest_framework import serializers
from . import models

class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'
