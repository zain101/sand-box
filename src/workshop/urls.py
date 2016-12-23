from django.conf.urls import url
from . import views

urlpatterns = [
	# url(r'^$',views.index, name="index"),
	url(r'^$',views.EventListView.as_view(), name="index"),
	url(r'^(?P<pk>[0-9]+)/$',views.EventDetailView.as_view(), name="detail"),
	url(r'^create$',views.event_create, name="create"),

	# url(r'^venue$',views.VenueListView.as_view(), name="venue_index"),
	# url(r'^venue/(?P<pk>[0-9]+)/$',views.VenueDetailView.as_view(), name="venue_detail"),
	# url(r'^venue/create$',views.venue_create, name="venue_create"),
]