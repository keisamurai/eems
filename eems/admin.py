from django.contrib import admin

# Register your models here.
from .models import Beacon_Log, Current_Entry, User_Master

admin.site.register(User_Master)
admin.site.register(Current_Entry)
admin.site.register(Beacon_Log)
