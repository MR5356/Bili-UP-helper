import os

import qtawesome
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtWidgets import qApp, QMessageBox, QAction, QSystemTrayIcon, QApplication, QMenu
from .threads import MainInfo_Thread
from UI.main import Ui_MainWindow
from .common import openBrowser
from . import defines


class fun_main(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, cookies):
        super(fun_main, self).__init__()
        self.setupUi(self)
        self.m_flag = False
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 主窗口透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowIcon(QIcon(':/images/logo.ico'))
        self.setWindowIconText(defines.title)
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 窗口始终置顶
        self.setWindowFlag(Qt.Tool)  # 隐藏任务栏图标
        self.signalOnButton()
        self.iconOnButton()
        self.simpleUI()
        self.init_systray()
        self.cookies = cookies
        # 线程启动
        self.mainThread()

    def signalOnButton(self):
        self.pushButton_close.clicked.connect(self.hide)
        self.pushButton_simple.clicked.connect(self.simpleUI)
        self.pushButton_signout.clicked.connect(self.signOut)
        self.pushButton_notify_sys_msg.clicked.connect(lambda: openBrowser("https://message.bilibili.com/#/system"))
        self.pushButton_notify_reply.clicked.connect(lambda: openBrowser("https://message.bilibili.com/#/reply"))
        self.pushButton_notify_like.clicked.connect(lambda: openBrowser("https://message.bilibili.com/#/love"))
        self.pushButton_notify_chat.clicked.connect(lambda: openBrowser("https://message.bilibili.com/#/whisper"))
        self.pushButton_notify_at.clicked.connect(lambda: openBrowser("https://message.bilibili.com/#/at"))
        # 暂时隐藏展开界面
        self.pushButton_simple.hide()
        # 通知栏按钮默认隐藏
        self.pushButton_notify_sys_msg.hide()
        self.pushButton_notify_reply.hide()
        self.pushButton_notify_like.hide()
        self.pushButton_notify_chat.hide()
        self.pushButton_notify_at.hide()

    # 测试
    def test(self):
        self.widget_video_sum.clicked.connect(lambda : print("123"))

    def iconOnButton(self):
        self.pushButton_close.setIcon(qtawesome.icon('fa.close', color='white'))
        self.pushButton_simple.setIcon(qtawesome.icon('fa.minus-square', color='white'))
        self.pushButton_signout.setIcon(qtawesome.icon('fa.sign-out', color='white'))
        self.pushButton_notify_at.setIcon(qtawesome.icon('fa.at', color='white'))
        self.pushButton_notify_chat.setIcon(qtawesome.icon('fa.commenting-o', color='white'))
        self.pushButton_notify_like.setIcon(qtawesome.icon('fa.thumbs-o-up', color='white'))
        self.pushButton_notify_reply.setIcon(qtawesome.icon('fa.reply', color='white'))
        self.pushButton_notify_sys_msg.setIcon(qtawesome.icon('fa.bullhorn', color='white'))

    # 任务栏托盘
    def init_systray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(':/images/logo.ico'))
        self.tray.setToolTip("哔哩哔哩UP主助手")
        self.tray.activated.connect(self.tray_act)  # 设置托盘点击事件处理函数
        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        self.tray_menu.setWindowFlags(self.tray_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.tray_menu.setStyleSheet('''QMenu::item {border-radius: 4px;padding: 8px 48px 8px 16px;background-color: transparent;}
                                        QMenu::item:selected { background-color:rgb(240,245,255);}   
        ''')
        self.NicknameAction = QAction('昵称', self)
        self.tray_coin = QAction("硬币：0")
        self.tray_balance = QAction("电池：0")
        self.tray_follower = QAction("粉丝：0")
        self.LogoutAction = QAction('退出登录', self)
        self.FeedbackAction = QAction("官方网站", self)
        self.RestoreAction = QAction('显示主界面', self)  # 添加一级菜单动作选项(还原主窗口)
        # self.UpdateAction = QAction('检查更新', self)
        self.QuitAction = QAction('退出程序', self)  # 添加一级菜单动作选项(退出程序)
        self.RestoreAction.triggered.connect(self.show)
        self.QuitAction.triggered.connect(self.winClose)
        self.LogoutAction.triggered.connect(self.signOut)
        self.FeedbackAction.triggered.connect(lambda: openBrowser("https://new.toodo.fun"))
        # self.UpdateAction.triggered.connect(lambda: self.update_thread(auto=False))
        self.tray_coin.setIcon(qtawesome.icon('fa.btc', color="blank"))
        self.tray_balance.setIcon(qtawesome.icon('fa.flash', color='blank'))
        self.tray_follower.setIcon(qtawesome.icon('fa.user', color='blank'))
        self.LogoutAction.setIcon(qtawesome.icon('fa.sign-out', color="blank"))
        self.FeedbackAction.setIcon(qtawesome.icon('fa.envelope-o', color="blank"))
        self.RestoreAction.setIcon(qtawesome.icon('fa.home', color='blank'))
        # self.UpdateAction.setIcon(qtawesome.icon('fa.refresh', color='blank'))
        self.QuitAction.setIcon(qtawesome.icon('fa.sign-out', color='blank'))
        self.tray_menu.addAction(self.NicknameAction)
        self.tray_menu.addAction(self.tray_coin)
        self.tray_menu.addAction(self.tray_balance)
        self.tray_menu.addAction(self.tray_follower)
        self.tray_menu.addAction(self.LogoutAction)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.FeedbackAction)
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        # self.tray_menu.addAction(self.UpdateAction)
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu)  # 设置系统托盘菜单
        # self.tray.messageClicked.connect(self.notify_clicked)
        self.tray.show()

    def tray_act(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.show()
            self.activateWindow()  # 将软件临时置顶

    def mainThread(self):
        try:
            self.main_thread = MainInfo_Thread(self.cookies)
            self.main_thread.thread_signal.connect(self.changeUI)
            self.main_thread.start()
        except Exception as e:
            QMessageBox.information(self, '小助手提示', f'程序运行异常，请确定网络连接是否正常，然后尝试重启客户端，如问题还未解决，请点击反馈按钮留言\n错误信息:\n{e}')

    def changeUI(self, msm):
        # self.pushButton_notify.setText("")
        self.pushButton_notify.hide()
        self.label_level.setText(f'等级：{msm.get("level", [0, 0, 0])[0]}')
        self.label_coins.setText(f"硬币\n{msm.get('coins')}")
        self.label_level_exp.setText(f"{msm.get('level', [0, 0, 0])[1]}/{msm.get('level', [0, 0, 0])[2]}")
        self.progressBar_exp.setValue(int(msm['level'][1] / msm['level'][2] * 100))
        self.label_follower.setText(f"粉丝\n{msm.get('follower')}")
        self.label_face.setPixmap(QPixmap(msm.get("face")))
        self.label_face.setScaledContents(True)
        self.label_face.setToolTip(f"{msm.get('nickname')}")
        self.label_creative.setText(f"创作力\n{msm.get('rating', [0, 0, 0])[0]}")
        self.label_influence.setText(f"影响力\n{msm.get('rating', [0, 0, 0])[1]}")
        self.label_credit.setText(f"信用分\n{msm.get('rating', [0, 0, 0])[2]}")
        self.label_brokerage.setText(f"贝壳\n{msm.get('brokerage')}")
        self.label_balance.setText(f"电池\n{msm.get('balance')}")
        self.label_default_bp.setText(f"B币\n{msm.get('default_bp')}")
        self.label_video_view.setText(f"播放\n{msm['video']['view']}")
        self.label_video_like.setText(f"点赞\n{msm['video']['like']}")
        self.label_video_coin.setText(f"投币\n{msm['video']['coin']}")
        self.label_video_reply.setText(f"评论\n{msm['video']['reply']}")
        self.label_video_danmaku.setText(f"弹幕\n{msm['video']['danmaku']}")
        self.label_video_share.setText(f"分享\n{msm['video']['share']}")
        self.label_video_favorite.setText(f"收藏\n{msm['video']['favorite']}")
        self.label_article_view.setText(f"阅读\n{msm['article']['view']}")
        self.label_article_like.setText(f"点赞\n{msm['article']['like']}")
        self.label_article_coin.setText(f"投币\n{msm['article']['coin']}")
        self.label_article_reply.setText(f"评论\n{msm['article']['reply']}")
        self.label_article_share.setText(f"分享\n{msm['article']['share']}")
        self.label_article_favorite.setText(f"收藏\n{msm['article']['favorite']}")
        self.NicknameAction.setText(f"{msm.get('nickname')}")
        self.tray_coin.setText(f"{msm.get('coins')}")
        self.tray_balance.setText(f"{msm.get('balance')}")
        self.tray_follower.setText(f"{msm.get('follower')}")
        # 消息处理
        if msm['notify']['at'] != 0:
            self.pushButton_notify_at.show()
            self.pushButton_notify_at.setToolTip(f"{msm['notify']['at']}条@我的消息")
        else:
            self.pushButton_notify_at.hide()
        if msm['notify']['chat'] != 0:
            self.pushButton_notify_chat.show()
            self.pushButton_notify_chat.setToolTip(f"{msm['notify']['chat']}条新的聊天")
        else:
            self.pushButton_notify_chat.hide()
        if msm['notify']['like'] != 0:
            self.pushButton_notify_like.show()
            self.pushButton_notify_like.setToolTip(f"{msm['notify']['like']}个新的点赞")
        else:
            self.pushButton_notify_like.hide()
        if msm['notify']['reply'] != 0:
            self.pushButton_notify_reply.show()
            self.pushButton_notify_reply.setToolTip(f"{msm['notify']['reply']}条新的回复")
        else:
            self.pushButton_notify_reply.hide()
        if msm['notify']['sys_msg'] != 0:
            self.pushButton_notify_sys_msg.show()
            self.pushButton_notify_sys_msg.setToolTip(f"{msm['notify']['sys_msg']}条新的系统消息")
        else:
            self.pushButton_notify_sys_msg.hide()

    def signOut(self):
        os.remove("cache/status.json")
        self.tray.hide()
        self.main_thread.stop()
        self.destroy()
        qApp.exit(-1)

    def winClose(self):
        qApp.exit()

    def simpleUI(self):
        minw, maxw = 320, 930
        if self.width() != minw:  # 380改为290，为更好的界面调度
            self.widget_right.hide()
            # self.setFixedSize(290, 640)  # 精简版界面尺寸
            self.resize(minw, 640)
            self.pushButton_simple.setIcon(qtawesome.icon('fa.plus-square', color='white'))
            self.pushButton_simple.setToolTip("展开界面")
        else:
            self.widget_right.show()
            # self.setFixedSize(930, 640)  # 默认界面尺寸
            self.resize(maxw, 640)
            self.pushButton_simple.setIcon(qtawesome.icon('fa.minus-square', color='white'))
            self.pushButton_simple.setToolTip("Mini界面")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
