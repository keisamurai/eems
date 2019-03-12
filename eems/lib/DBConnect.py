import sys
import os
import django

# libからインポート
from eems.lib import Const


def get_db_object(tbl_name):
    """
    description : djangoのデータベースにアクセスし、オブジェクトを返す
    input       : tbl_name -> テーブル名
                :     output      : obj -> 要求のあったオブジェクト
    """
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    from eems.models import User_Master, Beacon_Log

    if tbl_name == Const.TBL_USER_MASTER_NAME:
        try:
            tbl = User_Master.objects.all()
        except:
            print("[:ERROR:] getting table data failed")
            return
    elif tbl_name == Const.TBL_BEACON_LOG_NAME:
        try:
            tbl = Beacon_Log.objects.all()
        except:
            print("[:ERROR:] getting table data failed")
            return
    else:
        print("[:ERROR:] getting table data failed")
        return

    return tbl


def insert_info(tbl_name, dic_data):
    """
    description : データをDBに挿入する
    input       : tbl_name -> テーブル名
                : dic_data -> テーブルに挿入するデータ
    output      : True/False
    """
    # Django DB 接続
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    from eems.models import User_Master, Current_Entry, Beacon_Log

    rtn = False

    if tbl_name == Const.TBL_USER_MASTER_NAME:
        try:
            User_Master(
                user_id=dic_data['user_id'],
                line_id=dic_data['line_id'],
                user_name=dic_data['user_name'],
                company=dic_data['company'],
                department=dic_data['department'],
                num_entry=dic_data['num_entry'],
                user_img=dic_data['user_img']
            ).save()

        except:
            print("[:ERROR:] getting table data({0}) failed".format(tbl_name))
            return rtn

    elif tbl_name == Const.TBL_CURRENT_ENTRY_NAME:
        try:
            Current_Entry(
                line_id=dic_data['user_id'],
                line_name=dic_data['line_name'],
                user_img=dic_data['user_img'],
                entry_time=dic_data['entry_time'],
                leave_time=dic_data['leave_time']
            ).save()

        except:
            print("[:ERROR:] getting table data({0}) failed".format(tbl_name))
            return rtn

    elif tbl_name == Const.TBL_BEACON_LOG_NAME:
        try:
            Beacon_Log(
                reply_token=dic_data['reply_token'],
                line_id=dic_data['line_id'],
                timestamp=dic_data['timestamp'],
                hwid=dic_data['hwid'],
                enter_or_leave=dic_data['enter_or_leave']
            ).save()

        except:
            print("[:ERROR:] getting table data({0}) failed".format(tbl_name))
            return rtn
    else:
        print("[:ERROR:] No such table ({0})".format(tbl_name))
        return rnt

    rtn = True
    return rtn


def update_or_insert_data(tbl_name, dic_data):
    """
    description : テーブルにアクセスし、データが存在すればUPDATE,
                : データが存在しなければINSERTする
    input       :
                : tbl_name  -> 対象のテーブル名
                : dic_data  -> 辞書型データ
    output      : true/false
    """

    rtn = False

    # Django DB 接続
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    from eems.models import User_Master, Current_Entry

    if tbl_name == Const.TBL_USER_MASTER_NAME:
        try:
            rtn = User_Master.objects.update_or_create(
                user_id=dic_data['user_id'],
                line_id=dic_data['line_id'],
                user_name=dic_data['user_name'],
                line_name=dic_data['line_name'],
                company=dic_data['company'],
                department=dic_data['department'],
                num_entry=dic_data['num_entry'],
                user_img=dic_data['user_img'],
            )
        except:
            print("[:ERROR:] getting table data failed")
            return rtn

    if tbl_name == Const.TBL_CURRENT_ENTRY_NAME:
        try:
            rtn = Current_Entry.objects.update_or_create(
                line_id=dic_data['line_id'],
                line_name=dic_data['line_name'],
                user_img=dic_data['user_img'],
                entry_time=dic_data['entry_time'],
                leave_time=dic_data['leave_time']
            )
        except:
            print("[:ERROR:] getting table data failed")
            return rtn

    else:
        print("[:ERROR:] getting table data failed")
        return rtn

    return rtn
