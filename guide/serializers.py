from rest_framework import serializers
from . import models

class Business_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        fields = '__all__'

class Guide_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guide
        fields = '__all__'
class Address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'

class Guide_Requirement_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guide_Body_Requirement
        fields = '__all__'
        # depth = 1
# class Availability_Serializer(serializers.Serializer):

# class Shift_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Shift
#         fields = '__all__'
#
# class Shift_Requirement_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Shift_Requirement
#         fields = '__all__'
