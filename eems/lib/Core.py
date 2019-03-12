# =================================================
# /        |/        |/  \     /  | /      \
# HHHHHHHH/ HHHHHHHH/ HH  \   /HH |/HHHHHH  |
# HH |__    HH |__    HHH  \ /HHH |HH \__HH/
# HH    |   HH    |   HHHH  /HHHH |HH      \
# HHHHH/    HHHHH/    HH HH HH/HH | HHHHHH  |
# HH |_____ HH |_____ HH |HHH/ HH |/  \__HH |
# HH       |HH       |HH | H/  HH |HH    HH/
# HHHHHHHH/ HHHHHHHH/ HH/      HH/  HHHHHH/
# =================================================
# name        : Core.py
# description : 入退室管理システムのコアロジックを提供する
# =================================================
import sys
import os

sys.path.append(os.getcwd())

from eems.lib import DBConnect
from eems.lib import Const
from eems.lib import LineTools


class Core:
    def __init__(self):
        """コンストラクタ"""
        pass

    def simple_process(self, dic_data):
        """
        description : 入退室j情報を受け取り、タイプに合わせて動作する
        args        : dic_data -> 入退室情報
        return      : true / false
        """
        rtn = True
        # ---------------------
        # データ取得
        # ---------------------
        reply_token = dic_data['reply_token']
        line_name = dic_data['line_name']
        user_img = dic_data['user_img']
        entry_or_leave = dic_data['entry_or_leave']

        # ---------------------
        # 入退室処理
        # ---------------------
        if entry_or_leave == Const.LINE_ENTRY:
            # db にデータを挿入
            if not DBConnect.update_or_insert_data(Const.TBL_CURRENT_ENTRY_NAME, dic_data):
                rtn = False

                return rtn

        if entry_or_leave == Const.LINE_LEAVE:
            # db からデータを削除
            pass

        # ---------------------
        # Line通知
        # ---------------------
        text = "{0}".format(entry_or_leave)
        try:
            LineTools.reply_text(text, reply_token)
        except:
            rtn = False

        return rtn

    def exit_process(self):
        """
        description :
        args        :
        return      :
        """
        pass
