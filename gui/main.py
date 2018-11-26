# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(587, 436)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.client_button = QtWidgets.QPushButton(self.centralwidget)
        self.client_button.setGeometry(QtCore.QRect(120, 50, 341, 141))
        self.client_button.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.client_button.setObjectName("client_button")
        self.server_button = QtWidgets.QPushButton(self.centralwidget)
        self.server_button.setGeometry(QtCore.QRect(120, 210, 341, 131))
        self.server_button.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.server_button.setObjectName("server_button")
        self.host_label = QtWidgets.QLabel(self.centralwidget)
        self.host_label.setGeometry(QtCore.QRect(6, 390, 41, 21))
        self.host_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.host_label.setObjectName("host_label")
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setGeometry(QtCore.QRect(350, 390, 101, 21))
        self.port_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.port_label.setObjectName("port_label")
        self.host_text = QtWidgets.QLineEdit(self.centralwidget)
        self.host_text.setGeometry(QtCore.QRect(50, 390, 291, 23))
        self.host_text.setObjectName("host_text")
        self.port_text = QtWidgets.QLineEdit(self.centralwidget)
        self.port_text.setGeometry(QtCore.QRect(460, 390, 113, 23))
        self.port_text.setObjectName("port_text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Python Chat"))
        self.client_button.setText(_translate("MainWindow", "Cliente"))
        self.server_button.setText(_translate("MainWindow", "Servidor"))
        self.host_label.setText(_translate("MainWindow", "Host:"))
        self.port_label.setText(_translate("MainWindow", "Porta:"))

