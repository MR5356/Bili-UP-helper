import time
import qrcode
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from .common import Bilibili
import datetime


class Login_Thread(QThread):
    """
    登录界面
    负责扫码登录哔哩哔哩账号
    """
    thread_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        def getQRCode():
            req = requests.get("https://passport.bilibili.com/qrcode/getLoginUrl").json()
            if req.get('code') == 0:
                oauthKey = req['data']['oauthKey']
                qrcodeUrl = req['data']['url']
                qrCode = qrcode.QRCode()
                qrCode.add_data(qrcodeUrl)
                qrCode = qrCode.make_image(back_color="Transparent")
                qrCode.save("qrCode.png")
                return oauthKey
            return False

        oauthKey = getQRCode()
        self.thread_signal.emit({"code": -2})
        while True:
            if oauthKey:
                data = {
                    'oauthKey': oauthKey,
                    'gourl': "https://passport.bilibili.com/account/security"
                }
                req = requests.post("https://passport.bilibili.com/qrcode/getLoginInfo", data=data).json()
                if req['data'] == -4:  # 未扫码
                    self.thread_signal.emit({"code": -4})
                elif req['data'] == -2:  # 二维码过期，需要重新生成
                    oauthKey = getQRCode()
                    self.thread_signal.emit({"code": -2})
                elif req['data'] == -5:  # 已经扫码，等待确认
                    self.thread_signal.emit({"code": -5})
                else:
                    cookiesRaw = req['data']['url'].split('?')[1].split('&')
                    cookies = {}
                    for cookie in cookiesRaw:
                        key, value = cookie.split('=')
                        if key != "gourl" and key != "Expires":
                            cookies[key] = value
                    # print(cookies)
                    self.thread_signal.emit({"code": 0, "cookies": cookies})
                    break
                time.sleep(1)


class MainInfo_Thread(QThread):
    """
    负责循环获取哔哩哔哩创作中心数据
    """
    thread_signal = pyqtSignal(dict)

    def __init__(self, cookies):
        super().__init__()
        self.cookies = cookies
        self.Flag = True

    def run(self):
        client = Bilibili(self.cookies)
        client.getStaticInfo()  # 不用经常更新的数据
        count = 0
        while self.Flag:
            if (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).weekday() == 6 and datetime.datetime.strptime(str(datetime.datetime.now().date())+'16:30', '%Y-%m-%d%H:%M') < datetime.datetime.now() < datetime.datetime.strptime(str(datetime.datetime.now().date())+'21:30', '%Y-%m-%d%H:%M') and count % 20 == 0:
                client.getStaticInfo()  # 周日晚刷新
            if count % 20 == 0:
                client.getMainInfo()  # 实时更新的数据
                # print("刷新数据成功")
            client.getNotify()
            count += 1
            self.thread_signal.emit(client.mainInfo)
            # print(f"刷新成功{count}次")
            # print(client.mainInfo)
            time.sleep(10)

    def stop(self):
        self.Flag = False
