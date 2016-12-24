"""sandbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from workshop.views import mail_test
from venueapp.views import oauth2callback
import allauth
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='about.html')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^email_test/', mail_test),
    url(r'^profile/', include("profileapp.urls", namespace='profile')),
    url(r'^venue/', include("venueapp.urls", namespace='venue')),
    url(r'^event/', include("workshop.urls", namespace='workshop')),
    url(r'^oauth2callback/', oauth2callback, name='auth_uri'),

]