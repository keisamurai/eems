from rest_framework import routers
from .views import Current_EntryViewSet, Today_EntryViewSet, ReservationsViewSet, Reservations_TodayViewSet


router = routers.DefaultRouter()
router.register(r'Current_Entry', Current_EntryViewSet)
router.register(r'Today_Entry', Today_EntryViewSet)
router.register(r'reservations', ReservationsViewSet)
router.register(r'reservations_today', Reservations_TodayViewSet)
