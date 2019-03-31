from rest_framework import serializers

from .models import Reservations, Reservations_Today


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ('book_id', 'line_id', 'entry_day')


class Reservations_TodaySerializer(serializers.ModelSerializer):
    reservation_info = ReservationsSerializer()

    class Meta:
        model = Reservations_Today
        fields = ['reservation_info']
