from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse

import json
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
