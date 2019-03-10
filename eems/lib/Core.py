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

from logging import getLogger, FileHandler, Formatter, DEBUG
from eems.lib import DateCulc
from eems.lib import DBConnect
from eems.lib import Const
from eems.lib import LineTools


class Core:
    def __init__(self):
        """コンストラクタ"""
        pass

    def simple_process(self, entry_or_leave, timestamp):
        """
        description : 入退室のタイプを受け取り、タイプに合わせて動作する
        args        : entry_or_leave : entry or leave
                    : timestamp      : データを受け取った時点のタイムスタンプ
        return      : true / false
        """
        rtn = True

        # Line通知
        if ee_type == Const.LINE_ENTRY:
            text = "{0}[time:{1}]".format(ee_type, timestamp)
            LineTools.reply_text(text)
            return rtn

        # 入退室以外のタイプ
        return False

    def exit_process(self):
        """
        description :
        args        :
        return      :
        """
        pass
