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
