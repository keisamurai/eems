from django.contrib import admin

# Register your models here.
from .models import Beacon_Log, User_Master

admin.site.register(User_Master)
admin.site.register(Beacon_Log)
