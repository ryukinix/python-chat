# coding: utf-8

# standard library
import protocol
import socket
import sys
import queue
from datetime import datetime

# PyQt5 imports
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore


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
        self.messages = queue.Queue()

    def receive_messages(self):
        """Receptor de mensagens do servidor"""
        while True:
            yield protocol.Message.receive(self.socket)

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

    def close(self):
        self.socket.close()


class ClientController(QtCore.QThread):

    server_died_signal = QtCore.pyqtSignal()
    new_message_signal = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            for msg in self.client.receive_messages():
                self.client.messages.put(msg)
                self.new_message_signal.emit()
        except protocol.ClientClosedError:
            print("Servidor morreu!")
            self.server_died_signal.emit()


class ClientGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/client.ui', self)
        self.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Return"),  # send message shortcut
            self
        )
        self.shortcut.activated.connect(self.send)
        self.send_button.clicked.connect(self.send)
        self.client = Client()
        self.client_thread = ClientController(self.client)
        self.client_thread.server_died_signal.connect(self.critical_error)
        self.client_thread.new_message_signal.connect(self.receive)
        self.client_thread.start()
        self.destroyed.connect(self.client.close)

    def send(self):
        """Envia uma mensagem para o servidor como as informações da GUI"""
        subject = self.subject_text.text()
        message = self.message_text.toPlainText()
        name = self.name_text.text()
        self.message_text.clear()  # clean message_text field
        self.client.name = name
        if message:
            self.client.send_message(message, subject)

    def receive(self):
        """Recebe uma mensagem do servidor e atualiza a interface."""
        msg = self.client.messages.get()
        self.chat_text.insertPlainText(str(msg))
        self.chat_text.moveCursor(QtGui.QTextCursor.End)
        self.chat_text.ensureCursorVisible()

    def critical_error(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Uma merda enorme aconteceu!")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText("O servidor está desligado! Tente rodar server.py antes.")
        sys.exit(dlg.exec_())

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        try:
            main.client.connect()
        except ConnectionRefusedError:
            main.critical_error()
        main.show()
        saddr = protocol.socket_dest_address(main.client.socket)
        caddr = protocol.socket_source_address(main.client.socket)
        msg = f"Cliente conectado a {saddr} e recebendo resposta em {caddr}"
        main.statusBar().showMessage(msg)
        sys.exit(app.exec_())


if __name__ == '__main__':
    ClientGUI.run()
