# //////////////////////////////////////////////
# // name        : Utility.py
# // description : Lib全体で共通で利用するメソッド
# //////////////////////////////////////////////
import inspect
import os
import logging


def location():
    """
    description: この関数が呼ばれたモジュール名、コード名、行数を返す
    args       : NA
    return     : string
    """
    frame = inspect.currentframe().f_back
    return os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno


def log_debug(name_logger, text):
    """
    description: djangoで設定されているloggerを利用してログを出力する。(レベルはDEBUG)
    args       : name_logger -> loggerの名前 ex.'django'
               : text        -> logに出力するテキスト
    return     : 
    """
    logger = logging.getLogger(name_logger)
    logger.debug(text)

    return
