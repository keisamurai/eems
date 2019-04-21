from rest_framework import serializers

from .models import User_Master, Current_Entry, Today_Entry, Reservations, Reservations_Today


class User_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Master
        fields = ['id', 'line_id', 'user_name', 'line_name']
        # refer:https://qiita.com/suzuesa/items/30bcbe6a7b2b2de1df25
        # idの読み込み専用をオフ
        extra_kwargs = {'id': {'read_only': False}}


class Current_EntrySerializer(serializers.ModelSerializer):
    user_info = User_MasterSerializer()

    class Meta:
        model = Current_Entry
        fields = ['user_info']

    # ネストされたモデルのPOSTに対応させる
    # refer:https://qiita.com/suzuesa/items/30bcbe6a7b2b2de1df25
    def create(self, validated_data):
        # validated_dataにネストされたモデルのPOSTされたデータが格納されている
        user_info = validated_data.pop('user_info')
        user_info = User_Master.objects.get(pk=user_info['id'])
        ce = Current_Entry.objects.create(user_info=user_info, **validated_data)
        return ce


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
