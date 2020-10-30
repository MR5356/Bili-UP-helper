import os

import requests
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import qApp


def pic_cache(url):
    if os.path.exists(f"cache/{url.split('/')[-1]}"):
        pass
    else:
        pic = requests.get(url).content
        try:
            with open(f"cache/{url.split('/')[-1]}", "wb") as f:
                f.write(pic)
        except Exception as e:
            print(e)
            qApp.quit()
    return f"cache/{url.split('/')[-1]}"


def scale(num):
    return str(num) if num < 1000 else str(round(num / 1000, 1)) + "k" if num < 10000 else str(
        round(num / 10000, 1)) + "w"


def openBrowser(url):
    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


def verifyCookies(cookies):
    url = f"https://api.bilibili.com/x/space/myinfo"
    headers = {
        'Host': "api.bilibili.com",
        'cookie': cookies,
    }
    response = requests.get(url, headers=headers, timeout=10).json()
    if response.get("code") != -101:
        return True
    else:
        return False


class Bilibili:
    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.headers.update({"cookie": cookies})
        self.session.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"})
        self.mainInfo = {
            "nickname": "",
            "face": "",
            "coins": 0,
            "mid": "",
            "level": [],
            "follower": 0,
            "rating": [],
            "balance": 0,
            "brokerage": 0,
            "default_bp": 0,
            "video": {
                "view": 0,
                "like": 0,
                "coin": 0,
                "reply": 0,
                "danmaku": 0,
                "share": 0,
                "favorite": 0,
            },
            "article": {
                "view": 0,
                "reply": 0,
                "coin": 0,
                "favorite": 0,
                "like": 0,
                "share": 0,
            },
            "notify": {
                "at": 0,
                "chat": 0,
                "reply": 0,
                "like": 0,
                "sys_msg": 0,
            },
        }

    def network(self, method, url, retry=10, timeout=15, **kwargs):
        if method in ["get", "post"]:
            for _ in range(retry):
                try:
                    res = getattr(self.session, method)(url, timeout=timeout, **kwargs)
                    return res.json()
                except:
                    pass
        return None

    def getStaticInfo(self):
        headers = {
            "Host": "api.bilibili.com"
        }
        # 创作力
        url = "https://api.bilibili.com/studio/growup/web/up/rating/stat"
        res = self.network("get", url, headers=headers)
        if res and res.get("code") == 0:
            self.mainInfo["rating"] = [res['data']['creative'], res['data']['influence'], res['data']['credit']]

    def getNotify(self):
        headers = {
            "Host": "api.bilibili.com"
        }
        headers2 = {
            "Host": "api.vc.bilibili.com"
        }
        url = "https://api.bilibili.com/x/msgfeed/unread?build=0&mobi_app=web"
        res = self.network("get", url, headers=headers)
        if res and res.get("code") == 0:
            self.mainInfo['notify']['at'] = res['data']['at']
            self.mainInfo['notify']['reply'] = res['data']['reply']
            self.mainInfo['notify']['like'] = res['data']['like']
            self.mainInfo['notify']['sys_msg'] = res['data']['sys_msg']
        url = "https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread?unread_type=0&build=0&mobi_app=web"
        res = self.network("get", url, headers=headers2)
        if res and res.get("code") == 0:
            self.mainInfo['notify']['chat'] = res['data']['follow_unread'] + res['data']["unfollow_unread"]

    def getMainInfo(self):
        # 个人信息
        url = "https://api.bilibili.com/x/space/myinfo?jsonp=jsonp"
        headers = {
            "Host": "api.bilibili.com"
        }
        res = self.network("get", url, headers=headers)
        if res and res.get("code") == 0:
            self.mainInfo["nickname"] = res['data']['name']
            face = pic_cache(res['data']['face'])
            self.mainInfo["face"] = face
            self.mainInfo["coins"] = scale(res['data']['coins'])
            self.mainInfo["mid"] = res['data']['mid']
            self.mainInfo["level"] = [res['data']['level_exp']['current_level'],
                                      res['data']['level_exp']['current_exp'], res['data']['level_exp']['next_exp']]
            self.mainInfo["follower"] = scale(res['data']['following'])
        # 钱包有关
        url = "https://member.bilibili.com/x/web/elec/balance"
        headers2 = {
            "Host": "member.bilibili.com",
        }
        res = self.network("get", url, headers=headers2)
        if res and res.get("code") == 0:
            self.mainInfo["brokerage"] = scale(res["data"]["bpay_account"]["brokerage"])
            self.mainInfo["balance"] = scale(res["data"]['wallet']["sponsorBalance"])
            self.mainInfo["default_bp"] = scale(res["data"]["bpay_account"]["default_bp"])

        # 视频数据
        def getVideos(pn=1, view=0, like=0, coin=0, reply=0, danmaku=0, share=0, favorite=0):
            url = f"https://member.bilibili.com/x/web/archives?status=is_pubing%2Cpubed%2Cnot_pubed&pn={pn}&ps=10&coop=1"
            res = self.network("get", url, headers=headers2)
            if res and res.get("code") == 0:
                count = res['data']['page']['count']
                pn = res['data']['page']['pn']
                ps = res['data']['page']['ps']
                if count > 0:
                    for k in res['data']['arc_audits']:
                        view += k['stat']['view']
                        like += k['stat']['like']
                        coin += k['stat']['coin']
                        reply += k['stat']['reply']
                        danmaku += k['stat']['danmaku']
                        share += k['stat']['share']
                        favorite += k['stat']['favorite']
                    if pn * ps > count:
                        self.mainInfo['video']['view'] = scale(view)
                        self.mainInfo['video']['like'] = scale(like)
                        self.mainInfo['video']['coin'] = scale(coin)
                        self.mainInfo['video']['reply'] = scale(reply)
                        self.mainInfo['video']['danmaku'] = scale(danmaku)
                        self.mainInfo['video']['share'] = scale(share)
                        self.mainInfo['video']['favorite'] = scale(favorite)
                    else:
                        getVideos(pn + 1, view=view, like=like, coin=coin, reply=reply, danmaku=danmaku, share=share,
                                  favorite=favorite)

        getVideos()

        # 文章数据
        def getArticle(pn=1, view=0, reply=0, coin=0, favorite=0, like=0, share=0):
            url = f"https://api.bilibili.com/x/article/creative/article/list?group=0&sort=&pn={pn}&mobi_app=pc"
            res = self.network("get", url, headers=headers)
            if res and res.get("code") == 0:
                count = res['artlist']['page']['total']
                pn = res['artlist']['page']['pn']
                ps = res['artlist']['page']['ps']
                if count > 0:
                    for k in res['artlist']['articles']:
                        view += k['stats']['view']
                        reply += k['stats']['reply']
                        coin += k['stats']['coin']
                        favorite += k['stats']['favorite']
                        like += k['stats']['like']
                        share += k['stats']['share']
                    if pn * ps > count:
                        self.mainInfo['article']['view'] = scale(view)
                        self.mainInfo['article']['reply'] = scale(reply)
                        self.mainInfo['article']['coin'] = scale(coin)
                        self.mainInfo['article']['favorite'] = scale(favorite)
                        self.mainInfo['article']['like'] = scale(like)
                        self.mainInfo['article']['share'] = scale(share)
                    else:
                        getArticle(pn + 1, view=view, reply=reply, coin=coin, favorite=favorite, like=like, share=share)

        getArticle()


if __name__ == '__main__':
    cookies = "DedeUserID=314191627;DedeUserID__ckMd5=882828c87b70862a;SESSDATA=06540927%2C1619270123%2C7e528%2Aa1;bili_jct=8076d038bbbfa9af7095e45a36b0f541;"
    test = Bilibili(cookies)
    test.getMainInfo()
    print(test.mainInfo)
