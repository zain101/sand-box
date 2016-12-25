from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm, MemberForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Member
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):

	# instance = get_object_or_404(Member, slug=slug)
	
	user = request.user
	member = get_object_or_404(Member, user=user)

	member_form = MemberForm(request.POST or None, request.FILES or None, instance = member)
	user_form = UserForm(request.POST or None, request.FILES or None, instance = user)

	valid = True
	if member_form.is_valid():
		instance = member_form.save(commit = False)
		instance.save()
	else:
		valid = False

	if user_form.is_valid():
		print "abc"
		instance = user_form.save(commit = False)
		instance.save()
	else:
		valid = False

	if valid:
		messages.success(request, "Updated Successfully")

	contex = {
		'member_form' : member_form,
		'user_form' : user_form
	}

	return render(request, 'profileapp/form.html',contex)

@receiver(post_save, sender=User)
def redirect_update_profile(sender, **kwargs):
	redirect(reverse('profile:update'))