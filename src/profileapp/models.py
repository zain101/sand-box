from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.core.urlresolvers import reverse

class Member(models.Model):
	user = models.OneToOneField(User, related_name='user_member')
	location = models.CharField(max_length=100,blank=True)
	topic =  ArrayField(models.CharField(max_length=20),blank=True, null=True)
	isOrganizer = models.BooleanField(default=False)
	isVenue = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.user.username

#reciving User post save signal to make entry in Member Model
@receiver(post_save, sender=User)
def make_relation_with_member(sender, **kwargs):
	if kwargs.get('created', False):
		user = Member.objects.get_or_create(user=kwargs.get('instance'))

@receiver(post_save, sender=Member)
def get_calendar_token(sender, **kwargs):
	# user = Member.objects.get(user=kwargs.get('instance'))
	member = kwargs.get('instance')
	if member.isVenue:
		#TODO : check if calendar token of this user exist in db
		#if no then redirect to get authorization and token generation process
		print "TODO in profileapp/models.py"
		pass

	