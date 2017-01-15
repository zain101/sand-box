from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class AccessToken(models.Model):
	user = models.OneToOneField(User, related_name='user_token')
	accessToken= models.TextField()
	refreshToken=models.TextField(blank=True)
	tokenExpiry=models.DateTimeField(blank=True, null=True)
	syncToken = models.CharField(max_length=64, null=True, blank=True)
	def __unicode__(self):
		return self.user.username

class Calendar(models.Model):
	user = models.ForeignKey(User)
	calendarIdG = models.CharField(max_length=64)
	summary = models.CharField(max_length=256, blank=True)
	description = models.CharField(max_length=500, blank=True)
	location = models.CharField(max_length=500, blank=True)
	timeZone = models.CharField(max_length=100, blank=True)
	eventSyncToken = models.CharField(max_length=64, blank=True)
	updated = models.DateTimeField(auto_now=False, blank=True, null=True)
	lastSync = models.DateTimeField(auto_now=True)
	isSynced = models.BooleanField(default=False)

	def __unicode__(self):
		return self.summary

class CalendarEvent(models.Model):
	calendar = models.ForeignKey('Calendar')	
	eventIdG = models.CharField(max_length=64)
	status = models.CharField(max_length=50)
	htmlLink = models.URLField(max_length=200, blank=True)
	created = models.DateTimeField(auto_now=False, blank=True, null=True)
	updated = models.DateTimeField(auto_now=False, blank=True, null=True)
	summary = models.CharField(max_length=500, blank=True)
	start = models.DateTimeField(auto_now=False, blank=True, null=True)
	end = models.DateTimeField(auto_now=False, blank=True, null=True)
	transparency = models.BooleanField(default=False) #false for busy
	
	def __unicode__(self):
		if self.summary:
			return str(self.summary)
		else:
			return "Untitled event"