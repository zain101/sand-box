from django.contrib import admin
from .models import AccessToken, Calendar, CalendarEvent

admin.site.register(AccessToken)
admin.site.register(Calendar)
admin.site.register(CalendarEvent)
