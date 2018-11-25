# coding: utf-8

# standard library
import protocol
import socket
import sys
from datetime import datetime

# PyQt5 imports
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic


class Client(object):

    """Define uma classe para enviar mensagens para o Servidor"""

    def __init__(self,
                 name='Client',
                 host=protocol.HOST,
                 port=protocol.PORT):
        self.name = name
        self.host = host
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET,      # IPV4
            socket.SOCK_STREAM,  # TCP
        )

    def connect(self):
        """Conecta com o servidor"""
        return self.socket.connect((self.host, self.port))

    def send_message(self, message, subject=None):
        """Envia uma mensagem para o servidor"""
        m = protocol.Message(
            self.name,
            subject,
            message,
            datetime.now().strftime("%d/%m/%Y %X")
        )
        m.send(self.socket)


class ClientGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/client.ui', self)
        self.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Enter"),  # send message shortcut
            self
        )
        self.shortcut.activated.connect(self.send)
        self.send_button.clicked.connect(self.send)
        self.client = Client()

    def send(self):
        subject = self.subject_text.text()
        message = self.message_text.toPlainText()
        name = self.name_text.text()
        self.message_text.clear()
        self.client.name = name
        if message:
            self.client.send_message(message, subject)

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        main.show()
        main.client.connect()
        msg = "Cliente conectado a {}:{}".format(main.client.host,
                                                 main.client.port)
        main.statusBar().showMessage(msg)
        sys.exit(app.exec_())


if __name__ == '__main__':
    ClientGUI.run()
