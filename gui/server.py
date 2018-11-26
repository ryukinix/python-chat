# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/server.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(637, 480)
        self.centralwidget = QtWidgets.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.clients_list = QtWidgets.QListWidget(self.centralwidget)
        self.clients_list.setGeometry(QtCore.QRect(445, 30, 181, 421))
        self.clients_list.setObjectName("clients_list")
        self.chat_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.chat_text.setGeometry(QtCore.QRect(10, 30, 421, 421))
        self.chat_text.setObjectName("chat_text")
        self.clients_label = QtWidgets.QLabel(self.centralwidget)
        self.clients_label.setGeometry(QtCore.QRect(448, -1, 171, 31))
        self.clients_label.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.clients_label.setAlignment(QtCore.Qt.AlignCenter)
        self.clients_label.setObjectName("clients_label")
        self.chat_label = QtWidgets.QLabel(self.centralwidget)
        self.chat_label.setGeometry(QtCore.QRect(10, 0, 421, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chat_label.sizePolicy().hasHeightForWidth())
        self.chat_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.chat_label.setFont(font)
        self.chat_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chat_label.setAutoFillBackground(False)
        self.chat_label.setStyleSheet("font: 12pt \"Sans Serif\";\n"
"font.center {\n"
"    text-align: center;\n"
"    border: 3px solid green;\n"
"}")
        self.chat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chat_label.setObjectName("chat_label")
        ServerWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ServerWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "Python Chat Server"))
        self.chat_text.setHtml(_translate("ServerWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.clients_label.setText(_translate("ServerWindow", "Clientes"))
        self.chat_label.setText(_translate("ServerWindow", "Chat Logging"))

