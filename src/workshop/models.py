from django.db import models
from django.contrib.auth.models import User



class Member(models.Model):
	user = models.OneToOneField(User, related_name='user_member')
	

class Event(models.Model):
	pass


class Venue(models.Model):
	pass