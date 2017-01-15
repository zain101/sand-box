from django.shortcuts import render, get_object_or_404, redirect
from oauth2client.client import flow_from_clientsecrets
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.core.urlresolvers import reverse
import os
from oauth2client.client import AccessTokenCredentials
from .utils import get_service
from django.contrib.auth.decorators import login_required
from .models import AccessToken, Calendar, CalendarEvent
from django.contrib import messages

@login_required()
def oauth2callback(request):
	try:
		calendar_token = AccessToken.objects.get(user=request.user)
		messages.info(request, "Already Authenticated")
		return redirect('/')
	except AccessToken.DoesNotExist:
		pass

	BASE = os.path.dirname(os.path.abspath(__file__))
	client_secret_path = os.path.join(BASE, 'client_secret.json')
	
	flow = flow_from_clientsecrets(
		client_secret_path,
		scope=[
			'https://www.googleapis.com/auth/calendar',
			'https://www.googleapis.com/auth/userinfo.email',
		],
		redirect_uri='http://localhost:8000/oauth2callback',
		# include_granted_scopes=True
	)

	args = dict(request.GET)
	if not args.get('code', False):
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = args.get('code').pop()
		credentials = flow.step2_exchange(auth_code)

		token_model, created = AccessToken.objects.get_or_create(user=request.user)

		if created : 
			token_model.refreshToken = credentials.refresh_token
		else:
			print "It was already there, only new token created"
		token_model.accessToken = credentials.access_token
		token_model.tokenExpiry = credentials.token_expiry
		token_model.save()

	messages.success(request, "Authentication Successfull")

	return redirect(reverse('calendar_app:calendar_list'))

@login_required()
def calendar_events(request, calendar_id=None):

	if calendar_id:
		calendar_obj = Calendar.objects.get(pk=calendar_id)

		if calendar_obj.user != request.user:
			messages.warning(request,"403 Forbidden")
			return redirect(reverse('calendar_app:calendar_list'))
	
	events = CalendarEvent.objects.filter(calendar=calendar_obj)

	contex = {
		'events' : events,
		'calendar' : calendar_obj
	}

	return render(request, 'calendar_app/event_list.html', contex)

def sync_events(request, calendar_id, force_full_sync=False):

	calendar_obj = get_object_or_404(Calendar, pk=calendar_id)
	if calendar_obj.user != request.user:
		messages.warning(request,"403 Forbidden")
		return redirect(reverse('calendar_app:calendar_list'))

	calendar_id_g = calendar_obj.calendarIdG

	try:
		service = get_service(request)
	except AccessToken.DoesNotExist:
		return redirect(reverse('auth_uri'))

	lastSyncToken = calendar_obj.eventSyncToken
	if lastSyncToken and force_full_sync==False:
		eventsResult = service.events().list(
			calendarId=calendar_id_g,
			syncToken=lastSyncToken
		).execute()
	else:
		eventsResult = service.events().list(
			calendarId=calendar_id_g
		).execute()

	events = eventsResult.get('items', [])

	print "Events : ", events

	if events:
		for event in events:
			try:
				event_obj = CalendarEvent.objects.get(eventIdG=event['id'])
			except CalendarEvent.DoesNotExist:
				event_obj = CalendarEvent()
				event_obj.eventIdG = event['id']
				event_obj.calendar = calendar_obj

			event_obj.status = event.get('status','')
			
			# delete/cancelled events dont have start and end Date Time
			if event.get('status') != "cancelled":
				event_obj.start = event['start'].get('dateTime', '')
				event_obj.end = event['end'].get('dateTime', '')
				event_obj.created = event.get('created','')
				event_obj.updated = event.get('updated','')
				event_obj.htmlLink = event.get('htmlLink','')
				event_obj.summary = event.get('summary','')
				# print "done"
			else:
				print "Cancelled" + event['status']
			
			transparency = event.get('transparency','')
			if transparency == "transparent":
				event_obj.transparency = True
			else:
				event_obj.transparency = False
			
			event_obj.save()

	calendar_obj.eventSyncToken = eventsResult.get('nextSyncToken','')
	calendar_obj.isSynced = True
	calendar_obj.save()

	messages.success(request, "Events Sync Successfull of Calendar %s " % (calendar_obj.summary) )

	return redirect(reverse('calendar_app:calendar_events', kwargs= { 'calendar_id' : calendar_obj.pk}))

@login_required()
def sync_calendar_list(request):

	try:
		service = get_service(request)
	except AccessToken.DoesNotExist:
		return redirect(reverse('auth_uri'))

	access_token = AccessToken.objects.get(user=request.user)
	service = get_service(request)

	result = service.calendarList().list().execute()
	
	for calendar_item in result['items']:
		try:
			obj = Calendar.objects.get(calendarIdG=calendar_item['id'])
		except Calendar.DoesNotExist:
			obj = Calendar()
			obj.calendarIdG = calendar_item.get('id','')

		obj.user = request.user
		obj.summary = calendar_item.get('summary','')
		obj.description = calendar_item.get('description','')
		obj.location = calendar_item.get('location','')
		obj.timeZone = calendar_item.get('timeZone','')
		obj.save()

	#renew syncToken
	access_token.syncToken = result['nextSyncToken']
	access_token.save()

	messages.success(request, "Calendar List Sync Successfully")

	return redirect(reverse('calendar_app:calendar_list'))

@login_required()
def calendar_list(request):

	calendars = Calendar.objects.filter(user=request.user)
	
	contex = {
		'calendars' : calendars
	}

	return render(request, 'calendar_app/calendar_list.html', contex)