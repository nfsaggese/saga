from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser
from . import models
from . import serializers
from django.shortcuts import redirect
from extensions.agileCRM import agileCRM
# Create your views here.
class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)
@csrf_exempt
def add_guide(request, format=None):
	"""
	Create a new Guide
	"""
	# if request.method == 'GET':
	#     customers = Launch_Customer.objects.all()
	#     serializer = Launch_Customer_Serializer(customers, many=True)
	#     return JSONResponse(serializer.data)

	if request.method == 'POST':
		data = FormParser().parse(request)
		# print(data)<QueryDict: {u'website': [u'mysite.com'], u'phone_number': [u'3172097889'], u'first_name': [u'nick'], u'last_name': [u'nick2'], u'sub_launch': [u'True'], u'email': [u'nfsaggese@custom11.com']}>
		serializer = serializers.Guide_Serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			#run agile crm script here
			tags = ["launch-leadform",]

			if(data["sub_launch"]):
				tags.append("launch-participateInterest")
			else:
				tags.append("launch-updates")
			contact_data = {
				"lead_score": "150",
				"tags": tags,
				"properties": [
					{
						"type": "SYSTEM",
						"name": "first_name",
						"value": data["first_name"],
					},
					{
						"type": "SYSTEM",
						"name": "last_name",
						"value": data["last_name"],
					},
					{
						"type": "SYSTEM",
						"name": "email",
						"subtype": "work",
						"value": data["email"],
					},
					{
						"type": "SYSTEM",
						"name": "phone",
						"value": data["phone_number"],
					},
					{
						"type": "CUSTOM",
						"name": "Website",
						"value": data["website"],
					},
				]
			}
			agileCRM("contacts","POST", contact_data,"application/json")
			return JSONResponse(serializer.data, status=201)
			# return redirect(request.META.get('HTTP_REFERER'))
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def contact(request):
	if request.method == 'POST':
		data = FormParser().parse(request)
		serializer = serializers.Contact_Serializer(data=data)
		if serializer.is_valid():
			from django.core.mail import send_mail
			msg = {}
			msg['Subject'] = data["message"][:20]
			msg['From'] = 'launch-contact@mailman.saga.guide'
			msg['To'] = ["nick@saga.guide","george@saga.guide"]
			linebreak = "\n"
			msg["body"] = data["name"] + linebreak + data["email"] + linebreak + data["phone"] + linebreak + data["message"]
			send_mail(msg['Subject'],msg['body'],msg['From'], msg['To'],fail_silently=False)
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
