from django.contrib import admin

from .models import CustomeUser, StudentBookedSession, DeansSessionAvailability

admin.site.register(CustomeUser)
admin.site.register(StudentBookedSession)
admin.site.register(DeansSessionAvailability)
