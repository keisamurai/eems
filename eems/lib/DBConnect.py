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


def insert_info(tbl_name, dic_data, queryset=""):
    """
    description : データをDBに挿入する
    input       : tbl_name -> テーブル名
                : dic_data -> テーブルに挿入するデータ
                : queryset -> foreignKey定義のデータをセットする場合に利用する
    output      : True/False
    note        : 改善の余地あり
    """
    # Django DB 接続
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    from eems.models import User_Master, Current_Entry, Today_Entry, Beacon_Log, Reservations, Reservations_Today

    rtn = False

    if tbl_name == Const.TBL_USER_MASTER_NAME:
        try:
            User_Master(
                line_id=dic_data['line_id'],
                user_name=dic_data['user_name'],
                company=dic_data['company'],
                department=dic_data['department'],
                num_entry=dic_data['num_entry'],
                user_img=dic_data['user_img']
            ).save()

        except Exception as e:
            print("[:ERROR:] getting table data({0}) failed: {1} ".format(tbl_name, e))
            return rtn

    elif tbl_name == Const.TBL_CURRENT_ENTRY_NAME:
        if queryset == "":
            print("[:ERROR:] getting table data({0}) failed. No queryset".format(tbl_name))
            return rtn

        try:
            Current_Entry(
                # querysetには1つしか入っていない想定 + slicingしないとエラーになる
                user_info=queryset[0]
            ).save()

        except Exception as e:
            print("[:ERROR:] getting table data({0}) failed: {1}".format(tbl_name, e))
            return rtn

    elif tbl_name == Const.TBL_Today_ENTRY_NAME:
        if queryset == "":
            print("[:ERROR:] getting table data({0}) failed. No queryset".format(tbl_name))
            return rtn

        try:
            Today_Entry(
                # querysetには1つしか入っていない想定 + slicingしないとエラーになる
                user_info=queryset[0]
            ).save()

        except Exception as e:
            print("[:ERROR:] getting table data({0}) failed: {1}".format(tbl_name, e))
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

        except Exception as e:
            print("[:ERROR:] getting table data({0}) failed: {1}".format(tbl_name, e))
            return rtn

    elif tbl_name == Const.TBL_RESERVATIONS_NAME:
        try:
            Reservations(
                book_id=dic_data['book_id'],
                line_id=dic_data['line_id'],
                entry_day=dic_data['entry_day'],
            ).save()

        except Exception as e:
            print("[:ERROR:] getting table data({0}) failed: {1}".format(tbl_name, e))
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
    other       : テーブルに挿入する処理に改善の余地あり
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


def get_filter_data(tbl_name, key_name, value, foreign_key_name=""):
    """
    description : テーブル名とキー名を指定されたときに、与えられた値
    　　　　　　　　でフィルターした時のクエリセットを返す
    input       :
                : tbl_name  -> 対象のテーブル名
                : key_name  -> 対象のキー名
                : value     -> チェック対象値
                : foreign_key_name -> foreignkeyでフィルタする場合、foreignkey名を受け付ける
    output      : false/ queryset
    url:https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties
    """
    rtn = False

    # Django DB 接続
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    # --------------------------------------------------------------
    # !!!CAUSION!!! : need "global <valiables>" for use table
    # https://ja.stackoverflow.com/questions/40647/python%E3%81%A7exec%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E4%B8%AD%E3%81%AB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%82%92%E6%9B%B8%E3%81%8F%E3%81%A8nameerror%E3%81%AB%E3%81%AA%E3%82%8B
    # --------------------------------------------------------------
    exec_str = "from {0}.models import {1}; global {1}".format(Const.APP_NAME, tbl_name)

    # クエリ用文字列生成
    if not foreign_key_name == "":
        # foreignkeyを持つ場合は、フィルタ用文字列をそれ用に用意する必要がある
        # ex. from eems.models import User_Master; global User_Master; queryset = User_Master.objects.filter(user_info__line_id="dummy1")
        exec_str = exec_str + ";" + "queryset = {0}.objects.filter({1}__{2}=\"{3}\")".format(tbl_name, foreign_key_name, key_name, value)
    else:
        exec_str = exec_str + ";" + "queryset = {0}.objects.filter({1}=\"{2}\")".format(tbl_name, key_name, value)

    # クエリセット取得
    try:
        exec_rtn = {}
        exec(exec_str, {}, exec_rtn)
    except Exception as e:
        print("[:ERROR:] getting table data failed : {0}".format(e))
        return rtn

    queryset = exec_rtn['queryset']

    return queryset


def check_contain_data(tbl_name, key_name, value, foreign_key_name=""):
    """
    description : テーブル名とキー名を指定されたときに、与えられた値が
    　　　　　　　　データベースにあるかチェックする
    input       :
                : tbl_name  -> 対象のテーブル名
                : key_name  -> 対象のキー名
                : value     -> チェック対象値
                : foreign_key_name -> foreignkeyでフィルタする場合、foreignkey名を受け付ける
    output      : true/false
    url:https://stackoverflow.com/questions/1981524/django-filtering-on-foreign-key-properties
    """
    rtn = False

    if foreign_key_name == "":
        query_set = get_filter_data(tbl_name, key_name, value)
    else:
        query_set = get_filter_data(tbl_name, key_name, value, foreign_key_name)

    if not query_set:
        return rtn

    if query_set.count() == 0:
        # フィルターをかけたが0件の場合
        return rtn
    else:
        rtn = True

    return rtn


def delete_queryset(tbl_name, key_name, value, foreign_key_name=""):
    """
    description : テーブル名とキー名を指定されたときに、与えられた値
    　　　　　　　　でフィルターした時のクエリセットを削除する
    input       :
                : tbl_name  -> 対象のテーブル名
                : key_name  -> 対象のキー名
                : value     -> チェック対象値
                : foreign_key_name -> foreignkeyでフィルタする場合、foreignkey名を受け付ける
    output      : true/false
    """
    rtn = False

    # Django DB 接続
    sys.path.append(Const.PJ_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(Const.PJ_CONFIG))
    os.chdir(Const.EEMS_PJ_ROOT)

    django.setup()

    # --------------------------------------------------------------
    # !!!CAUSION!!! : need "global <valiables>" for use table
    # https://ja.stackoverflow.com/questions/40647/python%E3%81%A7exec%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E4%B8%AD%E3%81%AB%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%82%92%E6%9B%B8%E3%81%8F%E3%81%A8nameerror%E3%81%AB%E3%81%AA%E3%82%8B
    # --------------------------------------------------------------
    exec_str = "from {0}.models import {1}; global {1}".format(Const.APP_NAME, tbl_name)

    # クエリ用文字列生成
    if not foreign_key_name == "":
        # foreignkeyを持つ場合は、フィルタ用文字列をそれ用に用意する必要がある
        # ex. from eems.models import User_Master; global User_Master; queryset = User_Master.objects.filter(user_info__line_id="dummy1")
        exec_str = exec_str + ";" + "queryset = {0}.objects.filter({1}__{2}=\"{3}\")".format(tbl_name, foreign_key_name, key_name, value)
    else:
        exec_str = exec_str + ";" + "queryset = {0}.objects.filter({1}=\"{2}\")".format(tbl_name, key_name, value)

    # クエリセット取得
    try:
        exec_rtn = {}
        exec(exec_str, {}, exec_rtn)
    except Exception as e:
        print("[:ERROR:] getting table data failed : {0}".format(e))
        return rtn

    # クエリセット削除
    exec_rtn['queryset'].delete()
    rtn = True

    return rtn
