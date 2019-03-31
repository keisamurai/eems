from django.contrib import admin

# Register your models here.
from .models import Beacon_Log, Current_Entry, Today_Entry, User_Master, Reservations, Reservations_Today

admin.site.register(User_Master)
admin.site.register(Current_Entry)
admin.site.register(Today_Entry)
admin.site.register(Beacon_Log)
admin.site.register(Reservations)
admin.site.register(Reservations_Today)
