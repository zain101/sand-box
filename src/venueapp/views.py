from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Venue, CalendarToken
from .forms import VenueForm
from profileapp.models import Member
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .utils import get_service
from oauth2client import client


from oauth2client.client import flow_from_clientsecrets
import datetime
import os
from oauth2client.client import AccessTokenCredentials

class VenueListView(generic.ListView):
    template_name = 'venueapp/venue_list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        return Venue.objects.all()

class VenueDetailView(generic.DetailView):
    model = Venue
    template_name = 'venueapp/venue_detail.html'

@login_required()
def create(request):
	form = VenueForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Venue Added Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())

	contex = {
		'form' : form,
		'heading' : "Add Venue"
	}
	return render(request,'venueapp/form.html',contex)

class MyVenueListView(generic.ListView):
    template_name = 'venueapp/venue_list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        return Venue.objects.filter(user=self.request.user.user_member)

@login_required()
def venue_update(request, pk):
	#getting member object of current user
	user = Member.objects.filter(user=request.user)[0]

	if not user.isVenue:
		msg = """
			You are not a venue, become venue to create venue<br>
			To Become Venue go to <a href='%s'>link</a> and check on venue field
		""" % reverse('profile:update')
		messages.warning(request, msg)
		return HttpResponseRedirect(reverse('workshop:index'))


	instance = get_object_or_404(Venue, pk=pk)

	#checking of user is owener of event
	if instance.user != user:
		messages.warning(request, "You dont have permission to edit !!")
		return HttpResponseRedirect(reverse('venue:detail', kwargs={ 'pk':pk }))

	form = VenueForm(request.POST or None, request.FILES or None, instance = instance)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Updated Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	contex = {
		'form' : form,
	}
	return render(request,'venueapp/form.html',contex)

@login_required()
def calendar_events(request):
	
	try:
		service = get_service(request)
	except CalendarToken.DoesNotExist:
		return redirect(reverse('auth_uri'))

	now = datetime.datetime.utcnow().isoformat() + 'Z'

	eventsResult = service.events().list(
	calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
	orderBy='startTime').execute()
	events = eventsResult.get('items', [])

	contex = {
		'events' : events
	}

	return render(request, 'venueapp/calendar_event.html', contex)

@login_required()
def oauth2callback(request):

	try:
		calendar_token = CalendarToken.objects.get(user=request.user)
		return redirect('/')
	except:
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

		token_model, created = CalendarToken.objects.get_or_create(user=request.user)

		if created : 
			token_model.refresh_token = credentials.refresh_token
		else:
			print "It was already there, only new token created"
		token_model.access_token = credentials.access_token
		token_model.token_expiry = credentials.token_expiry
		token_model.save()

	return HttpResponseRedirect(reverse('venue:calendar_events'))

@login_required()
def create_test_event(request):

	try:
		service = get_service(request)
	except CalendarToken.DoesNotExist:
		return redirect(reverse('auth_uri'))
	
	event = {
	  'summary': 'Testing the API to insert event,',
	  'location': 'Thane',
	  'description': 'Event created by sandbox using your token',
	  'start': {
	    'dateTime': '2016-12-25T22:25:00-07:00',
	    'timeZone': 'Asia/Calcutta',
	  },
	  'end': {
	    'dateTime': '2016-12-27T22:30:00-07:00',
	    'timeZone': 'Asia/Calcutta',
	  },
	  # 'recurrence': [
	  #   'RRULE:FREQ=DAILY;COUNT=2'
	  # ],
	  # 'attendees': [
	  #   {'email': 'lpage@example.com'},
	  #   {'email': 'sbrin@example.com'},
	  # ],
	  # 'reminders': {
	  #   'useDefault': False,
	  #   'overrides': [
	  #     {'method': 'email', 'minutes': 24 * 60},
	  #     {'method': 'popup', 'minutes': 10},
	  #   ],
	  # },
	}

	event = service.events().insert(calendarId='primary', body=event).execute()
	return HttpResponse('Event created: check it <a href="%s">here</a>' % (event.get('htmlLink')))