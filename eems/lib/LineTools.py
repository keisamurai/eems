# ///////////////////////////////
# // name        : LineTools.py
# // description : Line用のツール
# ///////////////////////////////
import requests
import json
import os
import sys
import datetime
import logging

from django.utils import timezone
from django.conf import settings

sys.path.append(os.getcwd())

from logging import getLogger, FileHandler, Formatter, DEBUG
from eems.lib import DateCulc
from eems.lib import DBConnect
from eems.lib import Const
from eems.lib import Core

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageSendMessage, ButtonsTemplate, TemplateSendMessage,
    DatetimePickerTemplateAction, PostbackEvent, PostbackAction
)

# --------------------
# LineBot設定
# --------------------
# https://qiita.com/kotamatsuoka/items/472b455e5f9a6315d499
# line-bot-sdk-python: https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-echo/app.py
line_bot_api = LineBotApi(Const.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Const.LINE_CHANNEL_SECRET)


def assign_from_line_request(request):
    """
    description : line からのwebhookに対して、処理を振り分ける(QR-CODE対応)
    args        : request -> lineからのrequest
    return      : True/False
    """
    rtn = True

    logger = logging.getLogger('django')
    # --------------------
    # 署名検証
    # ※Lineサーバーからのリクエストか検証する
    # --------------------
    if not validate_sig(request):
        return False
    # --------------------
    # データ取得(from request)
    # --------------------
    # get request body as text
    request_json = json.loads(request.body.decode('utf-8'))
    # --------------------
    # データ取得(from Json)
    # --------------------
    if request.method == 'POST':
        for event in request_json['events']:
            reply_token = event['replyToken']
            message_type = event['type']
            line_id = event['source']['userId']

            if settings.DEBUG is True:
                logging.debug("[:debug:]{0}".format(event))

            # datetimepicker用の対応
            # https://qiita.com/nnsnodnb/items/d07a768eeea7be6cec02
            if event['type'] == 'postback':
                if settings.DEBUG is True:
                    logging.debug("[:debug:]{0}".format(event))

                # 「いいえ」が選択されている場合
                if event['postback']['data'] == "action=cancel&selectID=2":
                    reply_text('入室予定があればまたご連絡ください。', reply_token)
                    return True

                # 「はい」が選択されている場合
                date_postback = event['postback']['params']['date']

                core = Core.Core()
                # 予約番号生成
                book_id = core.make_reservation_num(line_id, date_postback)

                entry_day = date_postback

                # データ生成
                dic_data = {
                    "book_id": book_id,
                    "line_id": line_id,
                    "entry_day": entry_day,
                }

                path = './qrcode/qrcode_' + line_id + '.jpeg'
                # logger.debug(date_postback)
                try:
                    url_path = Const.URL_QRCODE
                    # qr_codeを生成し、情報をユーザーに返却+dbに格納する
                    core.qr_code_process(book_id, dic_data, path, url_path, reply_token)

                except Exception as e:
                    logger.debug("[:ERROR:]failed while qrcode_process:{0}".format(e))
                    logger.debug("[:ERROR:]failed while qrcode_process:{0}".format(date_postback))
                    return False

                return True

    else:
        logger.debug("[:ERROR:] request.method is not POST : {}".format(request.method))
        return rtn

    # --------------------
    # データ取得(データタイプ判定)
    # --------------------
    # メッセージリクエスト
    if message_type == 'message':
        # line 接続確認時(from line developpers)
        if reply_token == Const.LINE_CONNECT_CHECK_REP_TOKEN:
            return rtn

        # line 通常メッセージリクエスト
        # datetimepickerを返す
        else:
            reply_datetimepicker(reply_token)
            return rtn

    # Line Beaconからのリクエスト
    # 使っていない。。時間があるときに削除対応しゅる
    if message_type == 'beacon':
        # データ取得
        for event in request_json['events']:
            line_id = event['source']['userId']
            timestamp = event['timestamp']
            hwid = event['beacon']['hwid']
            enter_or_leave = event['beacon']['type']

        # line ユーザーのプロファイル取得
        profile = line_bot_api.get_profile(line_id)

        line_name = profile.display_name
        user_name = line_name
        user_img = profile.picture_url
        timestamp = timezone.now()
        # データ生成
        dic_data = {
            "reply_token": reply_token,
            "line_id": line_id,
            "line_name": line_name,
            "user_naem": user_name,
            "user_img": user_img,
            "timestamp": timestamp,
            "hwid": hwid,
            "enter_or_leave": enter_or_leave
        }
        print(dic_data)  # for debug

        # データ保存(DB)
        insert_request_log_tbl(dic_data)
        core = Core.Core()
        core.enter_leave_process(dic_data)
        return rtn

    # メッセージリクエスト、Beaconリクエスト以外
    rtn = False
    return rtn


def validate_sig(request):
    """
    description : X-Line-Signatureを検証する
    args        : body -> リクエストbody(request.body.decode('utf8'))
                : signature -> リクエストheader内のx-line-signature
    return      : True/False
    """
    logger = logging.getLogger('django')

    # request.METAでは、HTTTP_ prefixがつくことに注意
    # https://stackoverflow.com/questions/3889769/how-can-i-get-all-the-request-headers-in-django
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
        return True

    except Exception as e:
        logger.error('[:ERROR:] error while validating signature:{0}'.format(e))
        return False


def insert_request_log_tbl(dic_data):
    """
    description : Beacon_Logテーブルにrequestの内容を挿入する
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


def reply_text(text, reply_token):
    """
    description : Lineアプリにテキストで返答する
        reply_token (str): Lineアプリに返答するためのトークン
        text (str): 返答メッセージ
    return      : true/false
    """
    # 返答
    try:
        line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=text)
        )
    except:
        return False

    return True


def reply_img(imgpath, reply_token):
    """
    description : Lineアプリに画像で返答する
        reply_token (str): Lineアプリに返答するためのトークン
        imagpath (str): 返答する画像の保存されているパス
    return      : true/false
    """
    logger = logging.getLogger('django')

    # 返答
    try:
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(
                original_content_url=imgpath,
                preview_image_url=imgpath,
            )
        )
    except Exception as e:
        logger.debug("[:ERROR:]process failed. while replying image{0}".format(e))
        return False

    return True


def reply_datetimepicker(reply_token):
    """
    description : 日付選択アクションをユーザーに提供する
    args        : reply_token -> 返信用トークン
    https://qiita.com/nnsnodnb/items/d07a768eeea7be6cec02
    ドキュメント  https://developers.line.biz/en/reference/messaging-api/#datetime-picker-action
    """
    logger = logging.getLogger('django')

    date_picker = TemplateSendMessage(
        alt_text="this is a buttons template",
        template=ButtonsTemplate(
            text="Please select",
            title="入室予約をしすか？予約をする場合、「はい」を選択し、入室予定をご入力ください",
            actions=[
                DatetimePickerTemplateAction(
                    label='はい',
                    data="action=datetemp&selectId=1",
                    mode="date",
                ),
                PostbackAction(
                    label='いいえ',
                    data="action=cancel&selectID=2"
                )
            ]
        )
    )

    try:
        line_bot_api.reply_message(
            reply_token,
            date_picker
        )
        return True
    except Exception as e:
        logger.debug("[:ERROR:] process failed while send datetimepicker template:{0}".format(e))
        return False


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
