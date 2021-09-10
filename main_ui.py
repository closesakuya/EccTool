# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_water_mainwd(object):
    def setupUi(self, water_mainwd):
        if not water_mainwd.objectName():
            water_mainwd.setObjectName(u"water_mainwd")
        water_mainwd.resize(538, 361)
        water_mainwd.setContextMenuPolicy(Qt.DefaultContextMenu)
        water_mainwd.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.centralwidget = QWidget(water_mainwd)
        self.centralwidget.setObjectName(u"centralwidget")
        self.sel_pic_btn = QPushButton(self.centralwidget)
        self.sel_pic_btn.setObjectName(u"sel_pic_btn")
        self.sel_pic_btn.setGeometry(QRect(110, 10, 21, 28))
        self.sel_pic_lbl = QLineEdit(self.centralwidget)
        self.sel_pic_lbl.setObjectName(u"sel_pic_lbl")
        self.sel_pic_lbl.setGeometry(QRect(140, 10, 371, 21))
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(10, 10, 81, 21))
        self.sel_ecc_btn = QPushButton(self.centralwidget)
        self.sel_ecc_btn.setObjectName(u"sel_ecc_btn")
        self.sel_ecc_btn.setGeometry(QRect(110, 50, 21, 28))
        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(10, 50, 101, 21))
        self.sel_ecc_lbl = QLineEdit(self.centralwidget)
        self.sel_ecc_lbl.setObjectName(u"sel_ecc_lbl")
        self.sel_ecc_lbl.setGeometry(QRect(140, 50, 371, 21))
        self.result_lbl = QTextBrowser(self.centralwidget)
        self.result_lbl.setObjectName(u"result_lbl")
        self.result_lbl.setGeometry(QRect(10, 220, 501, 81))
        self.enc_btn = QPushButton(self.centralwidget)
        self.enc_btn.setObjectName(u"enc_btn")
        self.enc_btn.setGeometry(QRect(10, 170, 61, 41))
        self.sys_info_lbl = QLineEdit(self.centralwidget)
        self.sys_info_lbl.setObjectName(u"sys_info_lbl")
        self.sys_info_lbl.setGeometry(QRect(10, 120, 501, 31))
        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 100, 401, 21))
        self.dec_btn = QPushButton(self.centralwidget)
        self.dec_btn.setObjectName(u"dec_btn")
        self.dec_btn.setGeometry(QRect(100, 170, 61, 41))
        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(380, 90, 101, 21))
        self.sel_auth_btn = QPushButton(self.centralwidget)
        self.sel_auth_btn.setObjectName(u"sel_auth_btn")
        self.sel_auth_btn.setGeometry(QRect(490, 80, 21, 28))
        self.sign_lbl = QLineEdit(self.centralwidget)
        self.sign_lbl.setObjectName(u"sign_lbl")
        self.sign_lbl.setGeometry(QRect(420, 180, 91, 31))
        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(340, 190, 71, 21))
        self.open_when_fin_btn = QCheckBox(self.centralwidget)
        self.open_when_fin_btn.setObjectName(u"open_when_fin_btn")
        self.open_when_fin_btn.setGeometry(QRect(200, 190, 111, 19))
        water_mainwd.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(water_mainwd)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 538, 26))
        water_mainwd.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(water_mainwd)
        self.statusbar.setObjectName(u"statusbar")
        water_mainwd.setStatusBar(self.statusbar)

        self.retranslateUi(water_mainwd)

        QMetaObject.connectSlotsByName(water_mainwd)
    # setupUi

    def retranslateUi(self, water_mainwd):
        water_mainwd.setWindowTitle(QCoreApplication.translate("water_mainwd", u"\u56fe\u7247\u52a0\u5bc6\u5de5\u5177", None))
        self.sel_pic_btn.setText(QCoreApplication.translate("water_mainwd", u"...", None))
        self.sel_pic_lbl.setText(QCoreApplication.translate("water_mainwd", u"water-core", None))
        self.label_18.setText(QCoreApplication.translate("water_mainwd", u"\u56fe\u7247\u8def\u5f84:", None))
        self.sel_ecc_btn.setText(QCoreApplication.translate("water_mainwd", u"...", None))
        self.label_19.setText(QCoreApplication.translate("water_mainwd", u"\u52a0\u5bc6\u8f93\u51fa\u8def\u5f84:", None))
        self.sel_ecc_lbl.setText(QCoreApplication.translate("water_mainwd", u"water-core", None))
        self.enc_btn.setText(QCoreApplication.translate("water_mainwd", u"\u52a0\u5bc6", None))
        self.sys_info_lbl.setText(QCoreApplication.translate("water_mainwd", u"water-core", None))
        self.label_20.setText(QCoreApplication.translate("water_mainwd", u"\u8bc6\u522bID(\u8bf7\u5c06\u4ee5\u4e0bID\u53d1\u9001\u7ed9\u552e\u540e\u7533\u8bf7\u6388\u6743\u6587\u4ef6)\uff1a", None))
        self.dec_btn.setText(QCoreApplication.translate("water_mainwd", u"\u89e3\u5bc6", None))
        self.label_21.setText(QCoreApplication.translate("water_mainwd", u"\u52a0\u8f7d\u6388\u6743\u6587\u4ef6:", None))
        self.sel_auth_btn.setText(QCoreApplication.translate("water_mainwd", u"...", None))
        self.sign_lbl.setText(QCoreApplication.translate("water_mainwd", u"None", None))
        self.label_22.setText(QCoreApplication.translate("water_mainwd", u"\u52a0\u5bc6\u7b7e\u540d:", None))
        self.open_when_fin_btn.setText(QCoreApplication.translate("water_mainwd", u"\u5b8c\u6210\u540e\u6253\u5f00", None))
    # retranslateUi

