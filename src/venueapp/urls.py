from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', views.VenueListView.as_view(), name='index'),
	url(r'^my/$', login_required(views.MyVenueListView.as_view()), name='self_created'),
	url(r'^create$', views.create, name='create'),
	url(r'^(?P<pk>[0-9]+)/$',views.VenueDetailView.as_view(), name="detail"),
	url(r'^(?P<pk>[0-9]+)/edit$',views.venue_update, name="edit"),
	url(r'^calendar-events$',views.calendar_events, name="calendar_events"),
	url(r'^create-event$',views.create_test_event, name="calendar_create_event"),
]