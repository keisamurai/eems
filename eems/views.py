from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse

# for api
from django_filters import rest_framework
from rest_framework import viewsets, filters
from .serializer import User_MasterSerializer, Current_EntrySerializer, Today_EntrySerializer, ReservationsSerializer, Reservations_TodaySerializer

import json
import logging
from django_pandas.io import read_frame

from eems.models import *
from eems.lib import LineTools


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # ------------------
        # set user master infro
        # ------------------
        user_master = User_Master.objects.all()
        context['user_master'] = user_master

        # ------------------
        # set today entry info
        # ------------------
        today_entry = Today_Entry.objects.all()
        context['today_entry'] = today_entry

        # ------------------
        # set Entry Leave log info
        # ------------------
        entry_leave = Entry_Leave_Log.objects.all()
        context['entry_leave'] = entry_leave

        # ------------------
        # set current room info
        # ------------------
        current_entry = Current_Entry.objects.all()
        context['current_entry'] = current_entry

        # ------------------
        # set today entry info
        # ------------------
        today_entry = Today_Entry.objects.all()
        context['today_entry'] = today_entry

        # ------------------
        # set beacon log
        # ------------------
        with open('log/request.log') as log_file:
            log_txt = log_file.read()

        context['log_txt'] = log_txt

        return render(self.request, self.template_name, context)


class LogView(TemplateView):
    template_name = "log.html"

    def get(self, request, *args, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)

        # ------------------
        # set beacon log
        # ------------------

        # timestampにtimezoneを適用するために、read_frame()をつかうことはしない
        # ※read_frameをつかうと、テンプレート適用時にtimezoneが適用されない
        beacon_log = Beacon_Log.objects.all()
        context['beacon_log'] = beacon_log

        return render(self.request, self.template_name, context)


class Reservation_CalendarView(TemplateView):
    template_name = 'reservation_calendar.html'

    def get(self, request, *args, **kwargs):
        context = super(Reservation_TableView, self).get_context_data(**kwargs)

        # --------------------
        # set data
        # --------------------

        return render(self.request, self.template_name, context)


class Reservation_TableView(TemplateView):
    template_name = 'reservation_table.html'

    def get(self, request, *args, **kwargs):
        context = super(Reservation_TableView, self).get_context_data(**kwargs)

        # --------------------
        # set data
        # --------------------

        return render(self.request, self.template_name, context)


class User_MasterViewSet(viewsets.ModelViewSet):
    # http://www.tomchristie.com/rest-framework-2-docs/api-guide/filtering
    queryset = User_Master.objects.all()
    serializer_class = User_MasterSerializer
    filter_fields = ['id', 'line_id', 'user_name', 'line_name']


class Current_EntryViewSet(viewsets.ModelViewSet):
    # http://www.tomchristie.com/rest-framework-2-docs/api-guide/filtering
    queryset = Current_Entry.objects.all()
    serializer_class = Current_EntrySerializer
    filter_fields = ['user_info']


class Today_EntryViewSet(viewsets.ModelViewSet):
    # http://www.tomchristie.com/rest-framework-2-docs/api-guide/filtering
    queryset = Today_Entry.objects.all()
    serializer_class = Today_EntrySerializer
    filter_fields = ['user_info']


class ReservationsFilter(rest_framework.FilterSet):
    class Meta:
        model = Reservations
        fields = ['book_id', 'line_id', 'entry_day']


class ReservationsViewSet(viewsets.ModelViewSet):
    # http://www.tomchristie.com/rest-framework-2-docs/api-guide/filtering
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializer
    filter_fields = ['book_id', 'line_id', 'entry_day']


class Reservations_TodayViewSet(viewsets.ModelViewSet):
    # http://www.tomchristie.com/rest-framework-2-docs/api-guide/filtering
    queryset = Reservations_Today.objects.all()
    serializer_class = Reservations_TodaySerializer
    filter_fields = ['reservation_info']


def webhook(request):
    """Line Beaconのリクエストを受け取り、処理を実行する
    ref URL:https://qiita.com/__init__/items/8ae8401e9f0ff281ae64
    Args:
        request : Lineからのrequest
    Returns:
        : status = 200/500
    """
    # LineTools.request_log(request)   # for debuging
    result = LineTools.assign_from_line_request(request)

    if result:
        # ステータスコード 200を返却 (画面には何も表示しないのでなんでもいい)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)


def qrcode(request):
    """
    description : qrcodeの取得リクエストを受け取り、qrcod（image/jpeg)をhttpresponseで返す
    args        : Lineからのrequest
    """
    logger = logging.getLogger('django')

    path = './qrcode/qrcode_test.jpeg'
    try:
        qr = open(path, "rb").read()
        return HttpResponse(qr, content_type="image/jpeg")
    except Exception as e:
        logger.error("[:ERROR:]failed to respond qrcode:{0}".format(e))
        return HttpResponse(status_code=404)
