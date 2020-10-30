import qtawesome
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import qApp

from UI.login import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from function.common import openBrowser
from function import defines
from function.threads import Login_Thread
# from function import main


class login_UI(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(login_UI, self).__init__()
        self.setupUi(self)
        self.m_flag = False
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 窗口始终置顶
        self.pushButton_close.setIcon(qtawesome.icon('fa.close', color='blank'))
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_bottom.clicked.connect(lambda: openBrowser(defines.Login_bottom_url))
        self.pushButton_bottom.setText(defines.Login_bottom)
        self.pushButton_bottom.setToolTip(f"点击查看我的B站主页")
        self.label_version.setText(f"当前版本：{defines.version}")
        self.label_version.setToolTip(f"当前版本：{defines.version}")
        try:
            self.login_Thread = Login_Thread()
            self.login_Thread.thread_signal.connect(self.setQrcode)
            self.login_Thread.start()
        except Exception as e:
            print(f"Video Thread: {e}")

    def setQrcode(self, msm):
        if msm["code"] == -2:
            self.label_qrcode.setPixmap(QPixmap("qrCode.png"))
            self.label_qrcode.setScaledContents(True)
        elif msm["code"] == -5:
            self.label_qrcode.setText("已经扫码\n请在手机确认")
        elif msm["code"] == 0:
            cookies = ""
            for i in msm['cookies']:
                cookies += f"{i}={msm['cookies'][i]};"
            with open("cache/status.json", "w") as f:
                f.write(cookies)
            self.hide()  # 登录界面不会自动消失问题，程序重启前先进行隐藏界面操作
            qApp.exit(-1)
            # self.close()

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