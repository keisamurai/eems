# //////////////////////////////////////////////
# // name        : Const.py
# // description : Lib全体で共通で利用する定数定義
# //////////////////////////////////////////////
import sys
import os

# PJ-related
PJ_CONFIG = "config"
APP_NAME = "eems"
EEMS_PJ_ROOT = os.environ['EEMS_PJ_ROOT']  # pj root : D:\home\site\wwwroot\ (on Azure)

# DB-related
TBL_USER_MASTER_NAME = 'User_Master'
TBL_CURRENT_ENTRY_NAME = 'Current_Entry'
TBL_Today_ENTRY_NAME = 'Today_Entry'
TBL_Entry_Leave_Log_NAME = 'Entry_Leave_Log'
TBL_BEACON_LOG_NAME = 'Beacon_Log'

# Line-related
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN2"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET2"]
LINE_PUSH_ENDPOINT = 'https://api.line.me/v2/bot/message/push'
LINE_REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
LINE_CONNECT_CHECK_REP_TOKEN = "00000000000000000000000000000000"   # lineの接続確認用 replyToken
LINE_ENTRY = 'entry'
LINE_LEAVE = 'leave'
