from django.contrib import admin
from .models import User, Event, Participant, UploadedFetImage

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(UploadedFetImage)
