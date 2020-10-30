import sys
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox

sys.path.append("UI")
sys.path.append("./")
sys.path.append("function")

from PyQt5 import QtWidgets, QtCore, QtGui
from function.login import login_UI
from function.main import fun_main
from function.common import verifyCookies
from function import defines

def main():
    app = QtWidgets.QApplication(sys.argv)
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(":/images/start.png"))
    splash.setFont(QFont("microsoft yahei", 12, QFont.Normal))
    splash.showMessage("  正在初始化程序...", QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.black)
    splash.show()
    QtWidgets.qApp.processEvents()
    for i in defines.neededFolder:
        if not os.path.exists(i):
            os.mkdir(i)
    splash.showMessage("  正在检查登录状态...", QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.black)
    QtWidgets.qApp.processEvents()
    try:
        try:
            with open("cache/status.json", "r") as f:
                cookies = f.readline()
        except:
            cookies = ""
        if not verifyCookies(cookies):
            splash.showMessage("  登录状态失效，请重新登录", QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()
            # print("未登录")
            login_w = login_UI()
            login_w.show()
            splash.finish(login_w)
            login_w.activateWindow()
        else:
            splash.showMessage("  即将为您打开主程序", QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, QtCore.Qt.black)
            QtWidgets.qApp.processEvents()
            # print("已经登录")
            ui = fun_main(cookies)
            ui.show()
            splash.finish(ui)
            ui.activateWindow()
    except Exception as e:
        QMessageBox.information(None, '发生错误', f'请尝试重启应用\n{e}')
        sys.exit()
    exit_code = app.exec_()
    if exit_code == -1:
        main()
    else:
        sys.exit()


if __name__ == '__main__':
    main()
