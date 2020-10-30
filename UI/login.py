# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 640)
        Dialog.setStyleSheet("QDialog{background:Transparent;}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_main = QtWidgets.QWidget(Dialog)
        self.widget_main.setStyleSheet("QWidget#widget_main{border-image:url(:/images/login.png);border-radius:0px;background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #9796f0,stop:1 #fbc7d4);}")
        self.widget_main.setObjectName("widget_main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_top = QtWidgets.QWidget(self.widget_main)
        self.widget_top.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_top.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_top.setStyleSheet("QWidget#widget_top{background-color:rgba(255,255,255, 0.3);border-top-left-radius:0px;border-top-right-radius:0px;}")
        self.widget_top.setObjectName("widget_top")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_top)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_version = QtWidgets.QLabel(self.widget_top)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_version.setFont(font)
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.horizontalLayout.addWidget(self.label_version)
        spacerItem = QtWidgets.QSpacerItem(427, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_close = QtWidgets.QPushButton(self.widget_top)
        self.pushButton_close.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_close.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("QPushButton{background:Transparent;color:white;border:0px solid grey;border-radius:2px;}QPushButton:hover{background-color:rgba(90,135,228,0.5);border-radius:2px;}")
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addWidget(self.widget_top)
        self.widget_middle = QtWidgets.QWidget(self.widget_main)
        self.widget_middle.setStyleSheet("QWidget#widget_middle{background-color:rgba(255,255,255, 0);}")
        self.widget_middle.setObjectName("widget_middle")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_middle)
        self.verticalLayout_2.setContentsMargins(135, 170, 135, 190)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_qrcode = QtWidgets.QLabel(self.widget_middle)
        self.label_qrcode.setMinimumSize(QtCore.QSize(210, 210))
        self.label_qrcode.setMaximumSize(QtCore.QSize(210, 210))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_qrcode.setFont(font)
        self.label_qrcode.setText("")
        self.label_qrcode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_qrcode.setObjectName("label_qrcode")
        self.verticalLayout_2.addWidget(self.label_qrcode)
        self.verticalLayout.addWidget(self.widget_middle)
        self.widget_bottom = QtWidgets.QWidget(self.widget_main)
        self.widget_bottom.setMinimumSize(QtCore.QSize(0, 30))
        self.widget_bottom.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget_bottom.setStyleSheet("QWidget#widget_bottom{background-color:rgba(255,255,255, 0.3);border-bottom-left-radius:0px;border-bottom-right-radius:0px;}")
        self.widget_bottom.setObjectName("widget_bottom")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_bottom)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_bottom = QtWidgets.QPushButton(self.widget_bottom)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_bottom.setFont(font)
        self.pushButton_bottom.setStyleSheet("QPushButton{background:Transparent;color:Black;border:0px solid grey;}")
        self.pushButton_bottom.setText("")
        self.pushButton_bottom.setObjectName("pushButton_bottom")
        self.horizontalLayout_2.addWidget(self.pushButton_bottom)
        self.verticalLayout.addWidget(self.widget_bottom)
        self.gridLayout.addWidget(self.widget_main, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_close.setToolTip(_translate("Dialog", "<html><head/><body><p>关闭</p></body></html>"))
        self.pushButton_bottom.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
import resources_rc