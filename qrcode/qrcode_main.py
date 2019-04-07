# //////////////////////////////////////////////
# // name        : qrcode_main.py
# // description : カメラを起動させ、qrcodeを検知+読み込んで、
# //             :　予約番号がサーバーに登録されているかをチェックする
# //////////////////////////////////////////////
import cv2
import json
import requests
import datetime
from pyzbar.pyzbar import decode

NUMBER_OF_BOOKING_NUM = 32  # 予約番号の文字数


def api_curl(add_url):
    """
    description: api向けにcurlを実行しresponseを取得する
    args       : add_url -> request_urlに追加するurl
    return     : response
    """
    request_url = 'https://lbeacon.azurewebsites.net/api/reservations/{0}'.format(add_url)

    response = requests.get(request_url)

    return response


def check_booking_num(qr_data):
    """
    description: 予約番号かをチェックする
    args       : qr_data -> チェック対象の予約番号(str)
    return     : True/False
    """
    # ---------------------------
    # 簡易チェック:文字数
    # ---------------------------
    if not type(qr_data) is str:
        print("[:ERROR:]booking number should be string")
        return False

    if not len(qr_data) is NUMBER_OF_BOOKING_NUM:
        print("[:ERROR:]length of booking number should be 32 ")
        return False

    # ---------------------------
    # 照合チェック
    # ---------------------------
    # APIにクエリ

    flag = 0

    response = api_curl(data)
    if response.status_code == 404:
        print("[:ERROR:]No data")
        return False

    else response.status_code == 200:
        # json パース
        json_body = response.json()
        book_id = json_body[0]['book_id']
        line_id = json_body[0]['line_id']
        entry_day = json_body[0]['entry_day']

        # 予約番号確認
        if data == book_id:
            print('[:INFO:] Right Booking Number')
            # 日付確認
            if entry_day = datetime.datetime.now():
                print('[:INFO:] Right date')
                flag = 1

        if flag == 1:
            print('[:INFO:]You can enter room')
        else:
            return

    # api から予約されている日付を取得
    today_api = entry_day

    # 予約されている日付が本日日付であることをチェック
    today_system = datetime.datetime.today()
    today_system = datetime.datetime.strftime(today, "%Y-%m-%d")

    if today_api != today_system:
        print("[:INFO:]today_api != today_system")
        return False

    return True


def camera_read_qrcode(cam_num):
    """
    description: カメラを起動させ、QRコードを検知+読み込む
    args       : cam_num -> 起動させるカメラの番号(0:内臓カメラ, 1:外付けカメラ)
    return     : True/False
    # https://qiita.com/Oside/items/09eadb3b69d2b46c0ac2
    """
    cap = cv2.VideoCapture(cam_nam)  # ここでエラーを吐いたら ls /dev/video* を実行してカメラを認識しているか確認

    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        cv2.imshow("test", frame)  # GUIが使える時だけ
        gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
        data = decode(gray)
        for symbol in data:
            if symbol.type == "QRCODE":  # QRコード以外を読み取らないように
                qr_data = data[0][0].decode("utf-8", "ignore")
                print("[:INFO:]qrdata : {0}".format(qr_data))
                # ----------------------------
                # 予約番号を確認する
                # ----------------------------
                if check_booking_num(qr_data):
                    print("[:INFO:] welcome to our room!")
                else:
                    print("[:INFO:] please booking in ahead comming in")

        if cv2.waitKey(1) == 27:  # Escキーで終了(GUIがある場合のみ)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # camera qrcode読み取り
    NUM_CAMERA = 1  # カメラ番号:外付けカメラ
    camera_read_qrcode(NUMA_CAMERA)
