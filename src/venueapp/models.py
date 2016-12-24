from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Venue(models.Model):
	user = models.ForeignKey('profileapp.Member')
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
	confirmation = models.BooleanField(default=False)
	wifiAvailability = models.BooleanField(default=False)
	capacity = models.IntegerField(default=0)
	cateringAvailability = models.BooleanField(default=False)

	def __unicode__(self):
		return self.venueName

	def get_absolute_url(self):
		return reverse("venue:detail",kwargs = {"pk": self.id })

# class CalendarToken(models.Model):
# 	user = models.OneToOneField(User, related_name='user_venue')
# 	access_token= models.TextField()
# 	refresh_token=models.TextField(blank=True)
# 	token_expiry=models.DateTimeField(blank=True, null=True)