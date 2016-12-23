from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import EventForm
from django.contrib import messages
from django.views import generic
from .models import Event
from profileapp.models import Member
from django.contrib.auth.decorators import login_required

def mail_test(request):
	send_mail('Subject here', 'Here is the message.', 'fahad.shaikh091@gmail.com', ['fahad.shaikh091@gmail.com','fahad_shaikh09@yahoo.co.in'], fail_silently=False)
	
	return HttpResponse("testing")

def about(request):
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
	return render(request,'workshop/form.html',contex)

class EventListView(generic.ListView):
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all()

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'workshop/event_detail.html'