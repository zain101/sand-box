from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import EventForm
from django.contrib import messages
from django.views import generic
from .models import Event #,EventEnrolment
from profileapp.models import Member
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from allauth.account.decorators import verified_email_required


def mail_test(request):
	send_mail('Subject here', 'Here is the message.', 'fahad.shaikh091@gmail.com', ['fahad.shaikh091@gmail.com','fahad_shaikh09@yahoo.co.in'], fail_silently=False)
	
	return HttpResponse("testing")

@verified_email_required
def event_create(request):
	user = Member.objects.filter(user=request.user)[0]
	
	if not user.isOrganizer:
		msg = """
			You are not an organizer, become organizer to create events<br>
			To Become Organizer go to <a href='%s'>link</a> and check on organizer field
		""" % reverse('profile:update')
		messages.warning(request, msg)
		return HttpResponseRedirect(reverse('workshop:index'))

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
	return render(request,'workshop/form.html',contex)

@verified_email_required
def event_update(request,pk):

	#getting member object of current user
	user = Member.objects.filter(user=request.user)[0]

	if not user.isOrganizer:
		msg = """
			You are not an organizer, become organizer to create events<br>
			To Become Organizer go to <a href='%s'>link</a> and check on organizer field
		""" % reverse('profile:update')
		messages.warning(request, msg)
		return HttpResponseRedirect(reverse('workshop:index'))


	instance = get_object_or_404(Event, pk=pk)

	#checking of user is owener of event
	if instance.user != user:
		messages.warning(request, "You dont have permission to edit !!")
		return HttpResponseRedirect(reverse('workshop:detail', kwargs={ 'pk':pk }))

	form = EventForm(request.POST or None, request.FILES or None, instance = instance)

	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Updated Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	contex = {
		'form' : form,
	}
	return render(request,'workshop/form.html',contex)
	


class EventListView(generic.ListView):
    template_name = 'workshop/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().order_by('-schedule')

class MyEventListView(generic.ListView):
    template_name = 'workshop/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
    	return Event.objects.filter(user=self.request.user.user_member)

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'workshop/event_detail.html'

@verified_email_required
def enroll(request, pk):
	event = Event.objects.get(pk=pk)
	enrolled_events = request.user.event_set.all()
	print enrolled_events

	if not event in enrolled_events:
		event.enrolled_users.add(request.user)
		event.save()
		messages.info(request, "Successfully enrolled for the event '%s'" % (event.activityName) )
		return redirect(reverse('workshop:index'))
	else:
		messages.info(request, "You have already enrolled for this event")
		return redirect(reverse('workshop:index'))