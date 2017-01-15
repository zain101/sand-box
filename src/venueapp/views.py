from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Venue
from .forms import VenueForm
from profileapp.models import Member
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from allauth.account.decorators import verified_email_required

class VenueListView(generic.ListView):
    template_name = 'venueapp/venue_list.html'
    context_object_name = 'venues'

    def get_queryset(self):
        return Venue.objects.all()

class VenueDetailView(generic.DetailView):
    model = Venue
    template_name = 'venueapp/venue_detail.html'

@verified_email_required
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

@verified_email_required
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