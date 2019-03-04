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

        with open('log/request.log') as log_file:
            log_txt = log_file.read()
        # リクエスト空チェック
        # if(request_json != null):
        #     for event in request_json['events']:
        #         replytoken = event['replyToken']
        #         message_type = event['type']
        #         user_id = event['source']['userId']
        #         timestamp = event['timestamp']
        #         beacon_hwid = event['beacon']['hwid']
        #         beacon_type = event['beacon']['type']

        # --------------------
        # context　定義
        # --------------------
        # context['replytoken'] = replytoken
        context['log_txt'] = log_txt
        return render(self.request, self.template_name, context)


class LogView(TemplateView):
    template_name = "log.html"

    def get(self, request, *args, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)

        # ------------------
        # set beacon log
        # ------------------
        beacon_log = Beacon_Log.objects.all()
        df_beacon_log = read_frame(beacon_log)
        context['beacon_log'] = df_beacon_log

        return render(self.request, self.template_name, context)


def webhook(request):
    """Line Beaconのリクエストを受け取り、jsonファイルを生成する
    ref URL:https://qiita.com/__init__/items/8ae8401e9f0ff281ae64
    Args:
        request : Lineからのrequest
    Returns:
        : status = 200 を返却する
    """

    LineTools.request_log(request)
    LineTools.insert_request_log_tbl(request)

    # ステータスコード 200を返却 (画面には何も表示しないのでなんでもいい)
    return HttpResponse(status=200)
