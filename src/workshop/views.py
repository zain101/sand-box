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
import csv

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

@verified_email_required
def download_csv(request, pk):
	event = get_object_or_404(Event, pk=pk)

	filename = event.activityName +"_id" + str(event.id) + ".csv"

	if request.user.user_member != event.user:
		messages.warning(request, "You dont have permission to access this url")
		return redirect(reverse('workshop:detail', kwargs={'pk' : event.pk }))

	enrolled_users = event.enrolled_users.all()
	if not enrolled_users:
		messages.info(request, "No user have enrolled yet")
		return redirect(reverse('workshop:detail', kwargs={'pk' : event.pk }))

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)

	writer = csv.writer(response)
	
	writer.writerow(['Sr', 'Username', 'Email'])
	for i,enroll in enumerate(enrolled_users):
		writer.writerow([str(i+1), enroll.username , enroll.email])

	return response