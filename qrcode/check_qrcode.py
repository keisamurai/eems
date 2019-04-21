# test qr code
import cv2
import json
import requests
import datetime


def api_curl(add_url):
    """
    description: api向けにcurlを実行しresponseを取得する
    args       : add_url -> request_urlに追加するurl
    return     : response
    """
    request_url = 'https://lbeacon.azurewebsites.net/api/reservations/'

    response = requests.get(request_url)

    return response

if __name__ == '__main__':
    # -------------------------------------
    # QRコードから文字列を読み取る
    # https://algorithm.joho.info/programming/python/cv2-qrcodedetector/
    # -------------------------------------
    filename = './my_photo-4.jpg'

    # 入力画像のロード
    img = cv2.imread(filename)

    # データ、検出領域の四隅の座標、QRコードのバージョン情報を取得
    qr = cv2.QRCodeDetector()
    data, points, straight_qrcode = qr.detectAndDecode(img)

    print('data:', data)
    print('version', ((straight_qrcode.shape[0] - 21) / 4) + 1)
    # -------------------------------------
    # APIに照会をかける
    # -------------------------------------
    # APIにクエリ

    flag = 0

    response = api_curl(data)
    if response.status_code == 404:
        print("[:ERROR:]No data")
        return
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

        # beep

        # entry-leave log update
