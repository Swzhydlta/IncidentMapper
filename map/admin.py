from django.contrib import admin

# Register your models here.
from .models import User, Incident, editRequest

admin.site.register(User)
admin.site.register(Incident)
admin.site.register(editRequest)

