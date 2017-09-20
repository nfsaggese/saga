from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import api_view
from . import models
from . import serializers

# from helpers import availability

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)
# Create your views here.
@api_view(['POST','GET'])
def business(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)#parse incoming data
		print data
		serializer = serializers.Business_Serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
	elif request.method == 'GET':
		try:
			b = models.Business.objects.get(id=request.query_params['id'])
			serializer = Business_Serializer(b)
			return JSONResponse(serializer.data, status=200)
		except Business.DoesNotExist:
			return HttpResponse(status=404)
	elif request.method == 'PUT':

	elif request.method == 'DELETE':
		try:
			b = models.Business.objects.get(id=request.query_params['id'])
			b.delete()
		except Business.DoesNotExist:
			return HttpResponse(status=404)
	return JSONResponse(serializer.errors, status=400)

@api_view(['POST'])
def create_guide(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)#parse incoming data
		serializer = serializers.Guide_Serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
	return JSONResponse(serializer.errors, status=400)


@api_view(['POST'])
def create_address(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)#parse incoming data
		serializer = serializers.Address_Serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
	return JSONResponse(serializer.errors, status=400)
from helpers import availability

@api_view(['GET'])
def get_requirements_calendar(request):
	if request.method == 'GET':
		data = request.query_params
		r = availability.get_requirements_calendar(data["experience"],data["start"],data["end"])
		# print r#maybe build serializer
		print r
		return JSONResponse(r, status=201)
	return JSONResponse("Error",status=400)
# @api_view(['POST'])
# def create_shift(request):
# 	if request.method == 'POST':
# 		data = JSONParser().parse(request)#parse incoming data
# 		serializer = serializers.Shift_Serializer(data=data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JSONResponse(serializer.data, status=201)
# 	return JSONResponse(serializer.errors, status=400)
#
# @api_view(['POST'])
# def create_shift_requirement(request):
# 	if request.method == 'POST':
# 		data = JSONParser().parse(request)#parse incoming data
# 		serializer = serializers.Shift__Requirement_Serializer(data=data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return JSONResponse(serializer.data, status=201)
# 	return JSONResponse(serializer.errors, status=400)
