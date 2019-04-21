from rest_framework import serializers

from .models import User_Master, Current_Entry, Today_Entry, Reservations, Reservations_Today


class User_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Master
        fields = ['id', 'line_id', 'user_name', 'line_name']


class Current_EntrySerializer(serializers.ModelSerializer):
    user_info = User_MasterSerializer()

    class Meta:
        model = Current_Entry
        fields = ['user_info']


class Today_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Today_Entry
        fields = ['user_info']


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ('book_id', 'line_id', 'entry_day')


class Reservations_TodaySerializer(serializers.ModelSerializer):
    reservation_info = ReservationsSerializer()

    class Meta:
        model = Reservations_Today
        fields = ['reservation_info']
