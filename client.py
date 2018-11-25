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

    """Define uma classe para se comunicar com o Servidor"""

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
        self.socket.close()


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

    def run(self):
        """Função principal da thread. Quando executada esse método é iniciado."""
        try:
            for msg in self.client.receive_messages():
                self.client.messages.put(msg)
                self.new_message_signal.emit()
        except protocol.ClientClosedError:
            print("Servidor morreu!")
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
        msg = "Servidor morreu! Não é possível continuar a aplicação."
        self.client_thread.server_died_signal.connect(
            lambda: self.critical_error(msg)
        )
        self.client_thread.new_message_signal.connect(self.receive)
        self.destroyed.connect(self.client.close)
        self.message_text.setFocus()

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

    def critical_error(self, msg):
        """Erro crítico: servidor está morto. Deve finalizar a aplicação com um aviso."""
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Uma merda enorme aconteceu!")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText(msg)
        sys.exit(dlg.exec_())

    @classmethod
    def run(cls):
        """Inicializa a interface do sistema apropriadamente"""
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        try:
            main.client.connect()
        except ConnectionRefusedError:
            msg = "O servidor está desligado! Tente rodar server.py antes."
            main.critical_error(msg)
        main.show()
        main.client_thread.start()
        daddr = protocol.socket_dest_address(main.client.socket)
        saddr = protocol.socket_source_address(main.client.socket)
        msg = f"Cliente conectado a {daddr} e recebendo resposta em {saddr}"
        main.statusBar().showMessage(msg)
        sys.exit(app.exec_())


if __name__ == '__main__':
    ClientGUI.run()
