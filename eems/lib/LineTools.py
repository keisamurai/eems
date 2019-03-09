# ///////////////////////////////
# // name        : LineTools.py
# // description : Line用のツール
# ///////////////////////////////
import requests
import json
import os
import sys
import datetime

from django.utils import timezone

sys.path.append(os.getcwd())

from logging import getLogger, FileHandler, Formatter, DEBUG
from eems.lib import DateCulc
from eems.lib import DBConnect
from eems.lib import Const


def assign_from_line_request(request):
    """
    description : line からのwebhookに対して、処理を振り分ける
    args        : request -> lineからのrequest
    return      : True/False
    """
    rtn = True

    # --------------------
    # データ取得(from request)
    # --------------------
    request_json = json.loads(request.body.decode('utf-8'))
    # --------------------
    # データ取得(from Json)
    # --------------------
    if request.method == 'POST':
        for event in request_json['events']:
            reply_token = event['replyToken']
            message_type = event['type']
    else:
        return rtn

    # --------------------
    # データ取得(データタイプ判定)
    # --------------------
    # メッセージリクエスト
    if message_type == 'message':
        # line 接続確認時
        if reply_token == Const.LINE_CONNECT_CHECK_REP_TOKEN:
            return rtn
        # line 通常メッセージリクエスト
        else:
            # 処理したいことがあれば書く...
            return rtn

    # Line Beaconからのリクエスト
    if message_type == 'beacon':
        # データ取得
        for event in request_json['events']:
            user_id = event['source']['userId']
            timestamp = event['timestamp']
            hwid = event['beacon']['hwid']
            enter_or_leave = event['beacon']['type']

        # データ生成
        timestamp_date = DateCulc.DateFromMilli(timestamp)
        dic_data = {
            "reply_token": reply_token,
            "line_id": user_id,
            "timestamp": timezone.now(),
            "hwid": hwid,
            "enter_or_leave": enter_or_leave
        }

        # データ保存(DB)
        insert_request_log_tbl(dic_data)

        return rtn

    # メッセージリクエスト、Beaconリクエスト以外
    rtn = False
    return rtn


def insert_request_log_tbl(dic_data):
    """
    description : logテーブルにrequestの内容を挿入する
    args        : dic_data -> Lineからのbeaconリクエストに準ずる辞書データ
    return      : True/False
    """
    rtn = False

    # db アクセス
    if DBConnect.insert_info(Const.TBL_BEACON_LOG_NAME, dic_data):
        rtn = True
    else:
        return trn

    return rtn


def reply_text(reply_token, text):
    """
    name        : reply_text
    description : Lineアプリにテキストで返答する
        reply_token (str): Lineアプリに返答するためのトークン
        text (str): 返答メッセージ
    return      : true/false
    """
    # --------------
    # Header 生成
    # --------------
    HEADER = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Const.LINE_CHANNEL_ACCESS_TOKEN
    }

    # --------------
    # body 生成
    # --------------
    body = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': text
            }
        ]
    }

    # 返答
    try:
        requests.post(Const.LINE_REPLY_ENDPOINT, headers=HEADER, data=json.dums(body))
    except:
        return False

    return True


def request_log(request):
    """logging request for line
    Args:
        request (byte): ユーザーリクエストの情報
    """
    log_path = 'log/request.log'

    # for event in request['events']:
    #     timestamp = event['timestamp']
    # timestamp_date = DateCulc.DateFromMilli(timestamp)
    # timestamp = timestamp_date.strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        linelogger = getLogger('request_log')
        linelogger.setLevel(DEBUG)
        file_handler = FileHandler(log_path, 'a')
        file_handler.setLevel(DEBUG)
        linelogger.addHandler(file_handler)
        # linelogger.debug(timestamp)
        linelogger.debug(json.loads(request.body.decode('utf-8')))

    return
