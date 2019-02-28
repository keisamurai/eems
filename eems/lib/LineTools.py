# ///////////////////////////////
# // name        : LineTools.py
# // description : Line用のツール
# ///////////////////////////////
import requests
import json
import os
import datetime

from logging import getLogger, FileHandler, Formatter, DEBUG
from eems.lib import DateCulc

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


def request_log(request):
    """logging request for line
    Args:
        request (byte): ユーザーリクエストの情報
    """
    log_path = 'log/request.log'

    for event in request['events']:
        timestamp = event['timestamp']
    timestamp_date = DateCulc.DateFromMilli(timestamp)
    timestamp = timestamp_date.strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        linelogger = getLogger('request_log')
        linelogger.setLevel(DEBUG)
        file_handler = FileHandler(log_path, 'a')
        file_handler.setLevel(DEBUG)
        linelogger.addHandler(file_handler)
        linelogger.debug(timestamp)
        linelogger.debug(json.loads(request.body.decode('utf-8')))

    return
