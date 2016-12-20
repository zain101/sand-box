from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse


class Member(models.Model):
	user = models.OneToOneField(User, related_name='user_member')
	location = models.CharField(max_length=100)
	topic =  ArrayField(models.CharField(max_length=20))
	
	def __unicode__(self):
		return self.user.username

class Event(models.Model):
	activityName = models.CharField(max_length=200)
	activityType =  models.CharField(max_length=200)
	schedule = models.DateTimeField(auto_now_add=False)
	venue = models.ForeignKey('Venue')
	information = models.CharField(max_length=500,blank=True)
	content = models.TextField(blank=True)
	photo  = models.ImageField(blank=True)
	terms = models.TextField(blank=True)
	confirmation = models.BooleanField(default=False)
	cost = models.FloatField(default=0.0)
	user = models.ForeignKey('Member')

	def __unicode__(self):
		return self.activityName

	def get_absolute_url(self):
		return reverse("event_detail",kwargs = {"pk": self.id })


class Venue(models.Model):
	venueName = models.CharField(max_length=500)
	summary = models.CharField(max_length=1000)
	website = models.URLField(blank=True)
	socialLink = models.URLField(blank=True)
	coverPhoto = models.ImageField(blank=True)
	logo = models.ImageField(blank=True)
	contactInfo = models.CharField(max_length=200,blank=True)
	email = models.EmailField(max_length=254)
	location = models.CharField(max_length=500)
	phone = models.CharField(max_length=15)
	gmailCalender = models.CharField(max_length=500,blank=True)
	confirmation = models.BooleanField(default=False)
	wifiAvailability = models.BooleanField(default=False)
	capacity = models.IntegerField(default=0)
	cateringAvailability = models.BooleanField(default=False)

	def __unicode__(self):
		return self.venueName

	def get_absolute_url(self):
		return reverse("venue_detail",kwargs = {"pk": self.id })