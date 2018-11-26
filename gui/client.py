# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClientWindow(object):
    def setupUi(self, ClientWindow):
        ClientWindow.setObjectName("ClientWindow")
        ClientWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(ClientWindow)
        self.centralwidget.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 640, 461))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.subject_label = QtWidgets.QLabel(self.frame)
        self.subject_label.setGeometry(QtCore.QRect(10, 361, 91, 21))
        self.subject_label.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.subject_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.subject_label.setObjectName("subject_label")
        self.message_label = QtWidgets.QLabel(self.frame)
        self.message_label.setGeometry(QtCore.QRect(10, 390, 91, 61))
        self.message_label.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.message_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.message_label.setObjectName("message_label")
        self.name_label = QtWidgets.QLabel(self.frame)
        self.name_label.setGeometry(QtCore.QRect(10, 10, 71, 21))
        self.name_label.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        self.name_text = QtWidgets.QLineEdit(self.frame)
        self.name_text.setGeometry(QtCore.QRect(80, 10, 551, 23))
        self.name_text.setObjectName("name_text")
        self.subject_text = QtWidgets.QLineEdit(self.frame)
        self.subject_text.setGeometry(QtCore.QRect(110, 361, 451, 23))
        self.subject_text.setObjectName("subject_text")
        self.message_text = QtWidgets.QPlainTextEdit(self.frame)
        self.message_text.setGeometry(QtCore.QRect(110, 391, 451, 61))
        self.message_text.setTabChangesFocus(False)
        self.message_text.setPlainText("")
        self.message_text.setObjectName("message_text")
        self.send_button = QtWidgets.QPushButton(self.frame)
        self.send_button.setGeometry(QtCore.QRect(570, 361, 61, 91))
        self.send_button.setToolTip("")
        self.send_button.setObjectName("send_button")
        self.chat_text = QtWidgets.QTextBrowser(self.frame)
        self.chat_text.setGeometry(QtCore.QRect(10, 40, 621, 311))
        self.chat_text.setObjectName("chat_text")
        ClientWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ClientWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        ClientWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ClientWindow)
        QtCore.QMetaObject.connectSlotsByName(ClientWindow)

    def retranslateUi(self, ClientWindow):
        _translate = QtCore.QCoreApplication.translate
        ClientWindow.setWindowTitle(_translate("ClientWindow", "Python Chat Client"))
        self.subject_label.setText(_translate("ClientWindow", "Assunto"))
        self.message_label.setText(_translate("ClientWindow", "Mensagem"))
        self.name_label.setText(_translate("ClientWindow", "Nome "))
        self.name_text.setText(_translate("ClientWindow", "Manoel"))
        self.send_button.setText(_translate("ClientWindow", "Enviar"))

