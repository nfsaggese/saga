from django.shortcuts import render
from django.http import HttpResponse
import plivo, plivoxml
import os
from django.views.decorators.csrf import csrf_exempt
import base64,hmac
from hashlib import sha1
from django.urls import reverse
from guide import models

auth_id = os.environ['PLIVO_AUTH_ID']
auth_token = os.environ["PLIVO_AUTH_TOKEN"]
p = plivo.RestAPI(auth_id, auth_token)

root = "https://api.saga.guide"
def validate_signature(request, auth_token):
	uri = "https://" + request.META.get('SERVER_NAME')+request.META.get('REQUEST_URI')
	post_params = request.POST
	signature = request.META.get('HTTP_X_PLIVO_SIGNATURE')
	for k, v in sorted(post_params.items()):
		uri += k + v
	s = base64.encodestring(hmac.new(auth_token, uri, sha1).digest()).strip()
	return s == signature

@csrf_exempt
def call_guide(request, format=None):#Direction=inbound&From=13172097889&CallerName=%2B13172097889&BillRate=0.0085&To=13174275522&CallUUID=2e9856d8-135e-11e7-b774-dbf71cdc2903&CallStatus=ringing&Event=StartApp
	if request.method=="POST" and validate_signature(request, auth_token):
		intro = "Thank you for using Saga! Please enter the five digit code of the guide you wish to speak with."
		NO_INPUT_MESSAGE = "Sorry, I didn't catch that. Please hangup and try again later."
		r = plivoxml.Response()
		r.addSpeak(intro)
		getDigits = plivoxml.GetDigits(action=root + reverse('telecom:connect-guide'), method='POST', timeout=7, numDigits=5, retries=1)
		r.add(getDigits)
		r.addSpeak(NO_INPUT_MESSAGE)
		print r.to_xml()
		return HttpResponse(str(r),content_type="text/xml")

@csrf_exempt
def connect_guide(request):
	if request.method=="POST" and validate_signature(request, auth_token):
		r = plivoxml.Response()
		code = request.POST.get("Digits")#TODO route back to call guide if they enter in the wrong code (self referential?)
		print code
		guideName = "Nick Saggese" #TODO dynamically getting guidename and number, dynamically change number on page to track new users
		guideNumber = "13172964334"
		msg = "Please wait while we connect you to " + guideName + " This call may be recorded for quality assurance."
		r.addSpeak(msg)
		r.addDial(action=root+reverse('telecom:connect-guide-result'), method='POST', confirmKey="1", confirmSound=root + reverse('telecom:guide-accept-sound'), timeout=60, callerName="Saga", callerId="3174275522").addNumber(guideNumber)
		print r.to_xml()
		return HttpResponse(str(r),content_type="text/xml")
		#build in logic to get guide number from this

@csrf_exempt
def guide_accept_sound(request):
	if request.method=="POST" and validate_signature(request, auth_token):
		intro = "A potential customer is calling from Saga. Remember that this call is recorded. Please press 1 to connect."
		r = plivoxml.Response()
		r.addWait(length=2)
		r.addSpeak(intro)
		print r.to_xml()
		return HttpResponse(str(r),content_type="text/xml")

@csrf_exempt
def connect_guide_result(request):
	if request.method=="POST" and validate_signature(request, auth_token):

		if request.POST.get('DialStatus') == "completed":
			return HttpResponse("success")
		else:
			intro = "I'm sorry, but it looks like this guide is busy at the moment. It might be best to try again later. Thanks again for using Saga." #TODO lead monitoring and scheduling these calls, would be good to pass the guide name though
			r = plivoxml.Response()
			# r.addWait(length=2)
			r.addSpeak(intro)
			print r.to_xml()
			return HttpResponse(str(r),content_type="text/xml")
