from django.db import models
from django.core.urlresolvers import reverse
from profileapp.models import Member
from django.contrib.auth.models import User

class Event(models.Model):
	activityName = models.CharField(max_length=200)
	activityType =  models.CharField(max_length=200)
	schedule = models.DateTimeField(auto_now_add=False)
	venue = models.ForeignKey('venueapp.Venue')
	information = models.CharField(max_length=500,blank=True)
	content = models.TextField(blank=True)
	photo  = models.ImageField(blank=True)
	terms = models.TextField(blank=True)
	confirmation = models.BooleanField(default=False)
	cost = models.FloatField(default=0.0)
	user = models.ForeignKey('profileapp.Member')
	enrolled_users = models.ManyToManyField(User)

	def __unicode__(self):
		return self.activityName

	def get_absolute_url(self):
		return reverse("workshop:detail",kwargs = {"pk": self.id })