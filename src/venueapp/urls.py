from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.VenueListView.as_view(), name='index'),
	url(r'^create$', views.create, name='create'),
	url(r'^(?P<pk>[0-9]+)/$',views.VenueDetailView.as_view(), name="detail"),
]