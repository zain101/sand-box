from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.calendar_list, name="calendar_list"),
	url(r'^sync$',views.sync_calendar_list, name="sync_calendar_list"),
	url(r'^(?P<calendar_id>.*)/sync$',views.sync_events, name="sync_events"),
	url(r'^(?P<calendar_id>.*)/events/$', views.calendar_events, name='calendar_events'),
]