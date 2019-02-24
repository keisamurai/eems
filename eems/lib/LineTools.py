# ///////////////////////////////
# // name        : LineTools.py
# // description : Line用のツール
# ///////////////////////////////
import requests
import json
import os

from logging import getLogger, FileHandler, Formatter, DEBUG

# info
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/push'
CH_SECRET = '14938d0313af5d2729a1c5ecd5b4e03a'
ACCESSTOKEN = 'aUXuURYgoEkCHAX1EOER3da96MUOJwU7OKo39vSPiYuy0z/m+BPWTtjkINdaYJhKYryUo2YET5A8T+c4sKOa5BqdbCMgk4mE+uPsSodTLWiTHZMroZfk5Yn0oZTuJJDlHYIgOcyw3vt1tu+Bx1/B0AdB04t89/1O/w1cDnyilFU='

# header
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer' + ACCESSTOKEN
}


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
    log_path = 'log/request.json'

    if request.method == 'POST':
        linelogger = getLogger('request_json')
        linelogger.setLevel(DEBUG)
        file_handler = FileHandler(log_path, 'a')
        file_handler.setLevel(DEBUG)
        linelogger.addHandler(file_handler)
        linelogger.debug(json.loads(request.body.decode('utf-8')))

    return
