# ///////////////////////////////
# // name        : LineTools.py
# // description : Line用のツール
# ///////////////////////////////
import requests
import json
import os
import sys
import datetime

sys.path.append(os.getcwd())

from logging import getLogger, FileHandler, Formatter, DEBUG
from eems.lib import DateCulc
from eems.lib import DBConnect
from eems.lib import Const

# info
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/push'

# # header
# HEADER = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer' + ACCESSTOKEN
# }


def reply_text_beacon(reply_token, text):
    """
    description : line beacon用の応答メソッド
    args        : reply_token -> Lineに応答するためのトークンID
                : text        -> Line応答用テキスト
    return      : True/False
    """
    # bodyを作成
    body = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': text
            }
        ]
    }

    # リクエスト送信(POST)
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(body))
    return 'Complete'


def insert_request_log_tbl(request):
    """
    description : logテーブルにrequestの内容を挿入する
    args        : request -> Line サーバーからのPOSTデータ
    return      : True/False
    """
    rtn = False
    # --------------------
    # データ取得(from request)
    # --------------------
    request_json = json.loads(request.body.decode('utf-8'))
    print(request_json)
    # --------------------
    # データ取得(from Json)
    # --------------------
    if request.method == 'POST':
        evnet = request_json['events']

        reply_token = event['replyToken']
        message_type = event['type']
        user_id = event['source']['userId']
        timestamp = event['timestamp']
        hwid = event['beacon']['hwid']
        enter_or_leave = event['beacon']['type']
    else:
        return rtn

    # --------------------
    # データ挿入
    # --------------------
    timestamp_date = DateCulc.DateFromMilli(timestamp)
    dic_data = {
        "reply_token": reply_token,
        "line_id": user_id,
        "timestamp": timestamp_date,
        "hwid": hwid,
        "enter_or_leave": enter_or_leave
    }
    # db アクセス
    if DBConnect.insert_info(Const.TBL_BEACON_LOG_NAME, dic_data):
        rtn = True
    else:
        return trn

    return rtn


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
