from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$',views.EventListView.as_view(), name="index"),
	url(r'^my/$',login_required(views.MyEventListView.as_view()), name="self_created"),
	url(r'^(?P<pk>[0-9]+)/$',views.EventDetailView.as_view(), name="detail"),
	url(r'^(?P<pk>[0-9]+)/edit$',views.event_update, name="edit"),
	url(r'^create$',views.event_create, name="create"),
	url(r'^(?P<pk>[0-9]+)/enroll$',views.enroll, name="enroll"),
]