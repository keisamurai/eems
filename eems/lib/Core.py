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
import qrcode
import logging
import hashlib

sys.path.append(os.getcwd())

from eems.lib import DBConnect
from eems.lib import Const
from eems.lib import LineTools


class Core:
    def __init__(self):
        """コンストラクタ"""
        # loggerを生成
        logger = logging.getLogger('django')

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

    def enter_leave_process(self, dic_data):
        """
        description : 入退室情報を受け取り、タイプに合わせて動作する
        args        : dic_data -> 入退室情報
        return      : true / false
        """
        rtn = True
        # ---------------------
        # データ取得
        # ---------------------
        reply_token = dic_data['reply_token']
        line_id = dic_data['line_id']
        line_name = dic_data['line_name']
        user_img = dic_data['user_img']
        entry_or_leave = dic_data['entry_or_leave']
        print(dic_data)  # for debug

        # ---------------------
        # 入室処理
        # ---------------------
        if entry_or_leave == Const.LINE_ENTRY:
            # User_Masterに含まれるユーザーデータかをチェック
            key_name = "line_id"
            value = line_id

            flag_user_master = DBConnect.check_contain_data(
                Const.TBL_USER_MASTER_NAME,
                key_name,
                value
            )

            if flag_user_master:
                # ---------------------------------------------
                # User_Masterに含まれる場合、Current_Userに含まれるかチェック
                # ---------------------------------------------
                foreign_key_name = "user_info"

                flag_current_user = DBConnect.check_contain_data(
                    Const.TBL_CURRENT_ENTRY_NAME,
                    key_name,
                    value,
                    foreign_key_name=foreign_key_name
                )
            else:
                # ---------------------------------------------
                # User_Masterに含まれない場合、User_Masterに追加 + Current_User + Today_Entryに追加
                # ---------------------------------------------
                # User_Master用データ準備。使うことあるかも。。。
                dic_data['company'] = ""
                dic_data['department'] = ""
                dic_data['num_entry'] = 0

                # User_Masterに追加
                DBConnect.insert_info(Const.TBL_USER_MASTER_NAME, dic_data)

                # User_Masterからフィルターデータを取得
                queryset = DBConnect.get_filter_data(Const.TBL_USER_MASTER_NAME, key_name, line_id)
                if queryset:
                    # Current_Userに追加
                    rtn = DBConnect.insert_info(Const.TBL_CURRENT_ENTRY_NAME, dic_data, queryset=queryset)
                    return rtn
                else:
                    print("[:ERROR:]system failed to insert data:{0}".format(dic_data))
                    rtn = False
                    return rtn

                # User_Masterからフィルターデータを流用
                if queryset:
                    # Today_Entryに追加
                    rtn = DBConnect.insert_info(Const.TBL_Today_ENTRY_NAME, dic_data, queryset=queryset)
                    return rtn
                else:
                    # 多分どうやっても通らない処理..
                    print("[:ERROR:]system failed to insert data:{0}".format(dic_data))
                    rtn = False
                    return rtn

            if flag_current_user:
                # ---------------------------------------------
                # User_Masterに含まれ、Current_Userに含まれる場合、何もしない
                # ---------------------------------------------
                pass

            else:
                # ---------------------------------------------
                # User_Masterに含まれ、Current_Userに含まれない場合、Current_User + Today_Entryに追加
                # ---------------------------------------------
                queryset = DBConnect.get_filter_data(Const.TBL_USER_MASTER_NAME, key_name, line_id)
                if queryset:
                    # Current_Userに追加
                    DBConnect.insert_info(Const.TBL_CURRENT_ENTRY_NAME, dic_data, queryset=queryset)
                else:
                    print("[:ERROR:]system failed to insert data:{0}".format(dic_data))
                    rtn = False
                    return rtn

                # すでにToday_Entryにデータが追加されていないかチェック
                flag_today_entry = DBConnect.check_contain_data(
                    Const.TBL_Today_ENTRY_NAME,
                    key_name,
                    value,
                    foreign_key_name=foreign_key_name
                )

                if flag_today_entry:
                    # today_entryにすでにデータがある場合は何もしない
                    pass
                else:
                    # User_Masterからのフィルターデータを流用
                    if queryset:
                        # Today_Entryに追加
                        rtn = DBConnect.insert_info(Const.TBL_Today_ENTRY_NAME, dic_data, queryset=queryset)
                        return rtn
                    else:
                        # 多分どうやっても通らない処理..
                        print("[:ERROR:]system failed to insert data:{0}".format(dic_data))
                        rtn = False
                        return rtn

        # -------------
        # 退室処理
        # -------------
        if entry_or_leave == Const.LINE_LEAVE:

            # current_entryに対象データがあるかチェック
            flag_current = DBConnect.check_contain_data(Const.TBL_CURRENT_ENTRY_NAME, "line_id", line_id, foreign_key_name=foreign_key_name)
            if not flag_current:
                print("[:ERROR:]system failed while checking user id")
                rtn = False
                return rtn

            # db からデータを削除
            flag_delete = DBConnect.delete_queryset(Const.TBL_CURRENT_ENTRY_NAME, "line_id", line_id, foreign_key_name=foreign_key_name)
            if not flag_current:
                print("[:ERROR:]system failed to delete data while deleting queryset")
                rtn = False
                return rtn

        # ---------------------
        # Line通知(検証用に使う)
        # ---------------------
        text = "{0}".format(entry_or_leave)
        try:
            LineTools.reply_text(text, reply_token)
        except:
            rtn = False

        rtn = True
        return rtn

    def exit_process(self):
        """
        description :
        args        :
        return      :
        """
        pass

    def qr_code_process(self, text, dic_data, path, url_path, reply_token):
        """
        description : インプットされたテキストをQRCodeに変換し、ユーザーに返却する + DB予約情報を格納する
        args        : text -> QRコードに変換するテキスト
                    : dic_data -> DBに格納するデータ
                    : path -> QRコードを保存するパス
                    : url_path -> QRコードのパス(https)
                    : reply_token -> Lineの返信用トークン
        return      : true/false
        """
        rtn = False
        logger = logging.getLogger('django')

        try:
            logger.debug("[:DEBUG:] cwd :{0}".format(os.getcwd()))
            logger.debug("[:DEBUG:]:text:{0}".format(text))
            logger.debug("[:DEBUG:]:path:{0}".format(path))
            logger.debug("[:DEBUG:]:url_path:{0}".format(url_path))
            logger.debug("[:DEBUG:]:replay_toen:{0}".format(reply_token))

            # qrcode 生成
            qr = qrcode.make(text)
            qr.save(path)

            # 予約情報をDBに登録
            tbl_name = Const.TBL_RESERVATIONS_NAME
            DBConnect.insert_info(tbl_name, dic_data)

            # lineにて応答
            LineTools.reply_img(url_path, reply_token)
            rtn = True

        except Exception as e:
            print("[:ERROR:] getting error : {0}".format(e))
            logger.debug("[:ERROR:] getting error : {0}".format(e))
            return rtn

        return rtn

    def make_reservation_num(self, line_id, date_postback):
        """
        description: line_idと日付を入力に、md5で予約番号を生成する
        args       : line_id -> line id
                   : date_postback -> postback された日付
        return     : rn -> 予約番号
        """
        text = str(line_id) + str(date_postback)

        # MD5 hash
        hs_md5 = hashlib.md5(text.encode()).hexdigest()
        logger.debug("[:INFO:] debug : {0}".format(hs_md5))
        print("[:MD5:]{0}".format(hs_md5))

        return hs_md5
