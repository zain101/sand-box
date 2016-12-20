from django import forms
from .models import Venue, Event

class VenueForm(forms.ModelForm):
	class Meta:
		model = Venue
		fields = '__all__'

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['user',]