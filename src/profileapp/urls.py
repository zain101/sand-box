from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index, name="update"),
	# url(r'^event$',views.EventListView.as_view(), name="event_index"),
]