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

    from eems.models import User_Master, Beacon_Log

    rtn = False
    if tbl_name == Const.TBL_USER_MASTER_NAME:
        try:
            User_Master(
                user_id=dic_data['user_id'],
                line_id=dic_data['line_id'],
                user_name=dic_data['user_name'],
                company=dic_data['company'],
                department=dic_data['department']
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


# //////////////////////////
def update_or_insert_stock_data(pjname, tbl_name, stock_data, stock_code):
    """
    description : 株価データのテーブルにアクセスし、データが存在すればUPDATE,
                : データが存在しなければINSERTする
    input       : pjname -> PJ名(s3pj)
                : tbl_name -> テーブル名
                : stock_data -> 株価データ(DataFrame)
                : stock_code -> 対象株価データの銘柄コード
    output      : true/false
    """
    TBL_STOCK_NAME = "Stock"

    rtn = False

    sys.path.append(pjname)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(pjname))
    os.chdir(os.environ['S3_PJ_ROOT'])

    django.setup()

    from s3.models import Stock

    if tbl_name == TBL_STOCK_NAME:
        try:
            for i in range(len(stock_data)):
                rtn = Stock.objects.update_or_create(
                    code=stock_code,
                    date=stock_data['date'][i],
                    opening=stock_data['opening'][i],
                    high=stock_data['high'][i],
                    low=stock_data['low'][i],
                    closing=stock_data['closing'][i],
                    volume=stock_data['volume'][i],
                    adjustment=stock_data['adjustment'][i],
                )
        except:
            print("[:ERROR:] getting table data failed")
            return rtn
    else:
        print("[:ERROR:] getting table data failed")
        return rtn

    return rtn


def update_or_insert_sentiment_data(pjname, tbl_name, sentiment_data, stock_code):
    """
    description : センチメントデータのテーブルにアクセスし、データが存在すればUPDATE,
                : データが存在しなければINSERTする
    input       : pjname -> PJ名(s3pj)
                : tbl
                : stock_data -> センチメントデータ(DataFrame)
                : stock_code -> 対象センチメントデータの銘柄コード
    output      : true/false
    """
    TBL_SENTIMENT_NAME = "Sentiment"

    rtn = False

    # カレントディレクトリを退避
    cwd = os.getcwd()
    sys.path.append(pjname)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(pjname))
    os.chdir(os.environ['S3_PJ_ROOT'])

    django.setup()

    from s3.models import Sentiment

    if tbl_name == TBL_SENTIMENT_NAME:
        for i in range(len(sentiment_data)):
            try:
                rtn = Sentiment.objects.update_or_create(
                    code=stock_code,
                    name=sentiment_data['company name'][i],
                    date=sentiment_data['date'][i],
                    positive=sentiment_data['positive'][i],
                    neutral=sentiment_data['neutral'][i],
                    negative=sentiment_data['negative'][i]
                )
            except:
                print("[:ERROR:] getting table data failed")
                return rtn
    else:
        print("[:ERROR:] getting table data failed")
        return rtn

    # カレンとディレクトリを戻す
    os.chdir(cwd)

    return rtn
