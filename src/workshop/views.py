from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import VenueForm, EventForm
from django.contrib import messages
from django.views import generic
from .models import Event, Member, Venue
from django.contrib.auth.decorators import login_required


def mail_test(request):
	send_mail('Subject here', 'Here is the message.', 'fahad.shaikh091@gmail.com', ['fahad.shaikh091@gmail.com','fahad_shaikh09@yahoo.co.in'], fail_silently=False)
	
	return HttpResponse("testing")

def index(request):
	return render(request,'about.html',{})

@login_required()
def event_create(request):
	user = Member.objects.filter(user=request.user)[0]

	form = EventForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.user = user
		instance.save()
		messages.success(request, "Created Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())

	contex = {
		'form' : form,
		'heading' : "Add New Event"
	}
	return render(request,'form.html',contex)

class EventListView(generic.ListView):
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all()

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'event_detail.html'

class VenueListView(generic.ListView):
    template_name = 'venue_list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        return Venue.objects.all()

class VenueDetailView(generic.DetailView):
    model = Venue
    template_name = 'venue_detail.html'

@login_required()
def venue_create(request):

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
	return render(request,'form.html',contex)