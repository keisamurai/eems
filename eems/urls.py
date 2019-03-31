from rest_framework import routers
from .views import ReservationsViewSet, Reservations_TodayViewSet


router = routers.DefaultRouter()
router.register(r'reservations', ReservationsViewSet)
router.register(r'reservations_today', Reservations_TodayViewSet)
