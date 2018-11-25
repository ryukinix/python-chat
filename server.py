# coding: utf-8

import protocol
import socket
import sys
import queue
import threading

# PyQt5 imports
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import uic


class Server(object):

    """Servidor do sistema de chat"""

    def __init__(self, host=protocol.HOST, port=protocol.PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET,     # IPV4
            socket.SOCK_STREAM  # TCP
        )
        self.clients = []              # socket de clientes no sistema
        self.messages = queue.Queue()  # fila de mensagens

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def accept(self):
        return self.socket.accept()

    def close(self):
        for client in self.clients:
            client.close()
        self.socket.close()

    def send_broadcast(self, message):
        for client in self.clients:
            message.send(client)


class ServerController(QtCore.QThread):

    """Classe de interface entre Server <> ServerGUI"""

    message_signal = QtCore.pyqtSignal()
    new_client_signal = QtCore.pyqtSignal()
    deleted_client_signal = QtCore.pyqtSignal()

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        """Aceita conexões externas e dispara threads para leitura de mensagens"""
        while True:
            client, addr = self.server.accept()
            print("Cliente conectado: ", addr)
            self.server.clients.append(client)
            self.new_client_signal.emit()
            t = threading.Thread(target=self.read_message, args=(client,))
            t.start()

    def read_message(self, client):
        """Lê mensagens do cliente e coloca na fila Server.messages"""
        while True:
            try:
                msg = protocol.Message.receive(client)
                # print('Mensagem recebida de ', client)
                # print('Conteudo: ', msg)
                self.server.messages.put(msg)
                self.server.send_broadcast(msg)
                self.message_signal.emit()
            except protocol.ClientClosedError:
                print('Cliente fechou a conexão: ', client.getpeername())
                self.server.clients.remove(client)
                client.close()
                self.deleted_client_signal.emit()
                break


class ServerGUI(QtWidgets.QMainWindow):

    """Interface gráfica principal do sistema feita em Qt"""

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/server.ui', self)
        self.server = Server()
        self.server_thread = ServerController(self.server)
        self.server_thread.message_signal.connect(self.read_messages)
        self.server_thread.new_client_signal.connect(self.list_clients)
        self.server_thread.deleted_client_signal.connect(self.list_clients)

    def read_messages(self):
        msg = self.server.messages.get()
        self.chat_text.insertPlainText(str(msg))
        self.chat_text.moveCursor(QtGui.QTextCursor.End)
        self.chat_text.ensureCursorVisible()

    def list_clients(self):
        self.clients_list.clear()
        for client in self.server.clients:
            addr = protocol.socket_dest_address(client)
            item = QtWidgets.QListWidgetItem(addr)
            self.clients_list.addItem(item)

    def busy_port_error(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Uma merda enorme aconteceu!")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText(f"A porta {self.server.port} está ocupada! Tente outra.")
        sys.exit(dlg.exec_())

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        try:
            main.server.listen()
        except OSError:
            main.busy_port_error()

        main.show()
        msg = "Recebendo conexões em {}:{}".format(main.server.host,
                                                   main.server.port)
        main.statusBar().showMessage(msg)
        main.server_thread.finished.connect(app.exit)
        main.server_thread.start()
        main.destroyed.connect(main.server.close)
        sys.exit(app.exec_())


if __name__ == '__main__':
    ServerGUI.run()
