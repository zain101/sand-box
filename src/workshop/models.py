from django.db import models
from django.contrib.auth.models import User



class Member(models.Model):
	user = models.OneToOneField(User, related_name='user_member')
	location = # varchar
	topic =  # postgres list type

class Event(models.Model):
	activity_name = #varchar
	activity_type =  #varchar
	schedule = #Datetime
	venue = #FK to venue
	information = #varchar
	content = #varchar
	photos  = #blob or link
	terms = #varchar
	confirmation = #bool agree or not
	cost = #float
	user = #FK to member


class Venue(models.Model):
	venue_name = 
	summary =
	website = 
	social_link =
	cover_photo = 
	logo =
	contact_info = 
	email = 
	location = 
	phone = 
	gmail_calender = 
	confirmation = #bool
	wifi_avalibility = #bool
	capacity = 
	catering_avalible = #bool
	       