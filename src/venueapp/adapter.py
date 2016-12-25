from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages
from django.core.urlresolvers import reverse

class SocialAccountAdapter(DefaultSocialAccountAdapter):
	def save_user(self, request, sociallogin, form=None):
		super(SocialAccountAdapter, self).save_user(request, sociallogin, form=form)
		messages.info(request, "Welcome To Sandbox<br>To Complete Your Profile Goto \
		'Update Profile' tab from top right pull down menu or <a href='%s'>Click Here</a>" % (reverse('profile:update')))
		redirect(reverse('profile:update'))