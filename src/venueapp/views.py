from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Venue
from .forms import VenueForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class VenueListView(generic.ListView):
    template_name = 'workshop/venue_list.html'
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