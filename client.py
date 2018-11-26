# coding: utf-8

# standard library
import socket
import sys
import queue
from datetime import datetime

# PyQt5 imports
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import protocol
import gui.client


class Client(object):

    """Define uma classe para se comunicar com o Servidor"""

    def __init__(self, name='Client'):
        self.name = name
        self.host = protocol.HOST
        self.port = protocol.PORT
        self.socket = socket.socket(
            socket.AF_INET,      # IPV4
            socket.SOCK_STREAM,  # TCP
        )
        self.messages = queue.Queue()

    def connect(self):
        """Conecta com o servidor"""
        return self.socket.connect((self.host, self.port))

    def receive_messages(self):
        """Receptor de mensagens do servidor"""
        while True:
            yield protocol.Message.receive(self.socket)

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
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except OSError:
            # print("Cliente: Tentativa de desligar um socket não conectado.")
            pass


class ClientController(QtCore.QThread):

    """Thread para rodar em background na interface.

    Realiza leitura das mensagens enviadas pelo servidor
    e dispara dois sinais:

    + server_died_signal
    + new_message_signal

    Quando uma nova mensagem é recebida, esta mensagem é inserida
    na fila thread-safe client.messages. Então é emitido o sinal
    new_message_signal para que a interface atualize a tela de chat.

    Quando server_died_signal é disparado, a aplicação deve morrer com
    um aviso de que o servidor foi fechado/desconectado.
    """

    server_died_signal = QtCore.pyqtSignal()
    new_message_signal = QtCore.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.closed = False

    def run(self):
        """Função principal da thread. Quando executada esse método é iniciado."""
        try:
            for msg in self.client.receive_messages():
                self.client.messages.put(msg)
                self.new_message_signal.emit()
        except protocol.ClientClosedError:
            if not self.closed:
                print("Cliente: Servidor morreu!")
                self.server_died_signal.emit()


class ClientGUI(QtWidgets.QMainWindow):

    """Interface principal da tela de cliente.

    + ClientGUI.send envia uma nova mensagem para o servidor com os
      atuais campos preenchidos na interface. O campo mensagem é limpo
      após essa operação.
    + ClientGUI.receive consome a mensagem lida pela thread ClientController,
      disponível na fila self.client.messages
    + ClientGUI.critical_error exibe uma mensagem de erro crítico

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = gui.client.Ui_ClientWindow()
        self.ui.setupUi(self)
        self.ui.shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Return"),  # send message shortcut
            self
        )
        self.ui.shortcut.activated.connect(self.send)
        self.ui.send_button.clicked.connect(self.send)
        self.client = Client()
        self.client_thread = ClientController(self.client)
        msg_died = "Servidor morreu! Não é possível continuar a aplicação."
        self.client_thread.server_died_signal.connect(
            lambda: self.critical_error(msg_died)
        )
        self.client_thread.new_message_signal.connect(self.receive)
        self.ui.message_text.setFocus()

    def closeEvent(self, event):
        self.client_thread.closed = True
        self.client.close()
        parent = self.parent()
        if not parent:
            sys.exit()

    def init_client(self):
        try:
            self.client.connect()
            daddr = protocol.socket_dest_address(self.client.socket)
            saddr = protocol.socket_source_address(self.client.socket)
            msg_status = f"Cliente conectado a {daddr} e recebendo resposta em {saddr}"
            self.client_thread.start()
            self.statusBar().showMessage(msg_status)
            self.show()
        except ConnectionRefusedError:
            msg_server = "O servidor está desligado! Tente rodar server.py antes."
            self.critical_error(msg_server)

    def send(self):
        """Envia uma mensagem para o servidor como as informações da GUI"""
        subject = self.ui.subject_text.text()
        message = self.ui.message_text.toPlainText()
        name = self.ui.name_text.text()
        self.ui.message_text.clear()  # clean message_text field
        self.client.name = name
        if message:
            self.client.send_message(message, subject)

    def receive(self):
        """Recebe uma mensagem do servidor e atualiza a interface."""
        msg = self.client.messages.get()
        self.ui.chat_text.insertPlainText(str(msg))
        self.ui.chat_text.moveCursor(QtGui.QTextCursor.End)
        self.ui.chat_text.ensureCursorVisible()

    def critical_error(self, msg):
        """Erro crítico: servidor está morto. Deve finalizar a aplicação com um aviso."""
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Uma merda enorme aconteceu!")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText(msg)
        dlg.exec_()
        self.close()

    @classmethod
    def run(cls):
        """Inicializa a interface do sistema apropriadamente"""
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        main.init_client()
        sys.exit(app.exec_())


if __name__ == '__main__':
    ClientGUI.run()
