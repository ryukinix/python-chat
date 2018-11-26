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

    def __init__(self):
        self.host = protocol.HOST
        self.port = protocol.PORT
        self.socket = socket.socket(
            socket.AF_INET,     # IPV4
            socket.SOCK_STREAM  # TCP
        )
        self.clients = []              # socket de clientes no sistema
        self.messages = queue.Queue()  # fila de mensagens
        self.closed = False

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def accept(self):
        return self.socket.accept()

    def close(self):
        print("Servidor: Servidor sendo fechado!")
        for client in self.clients:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except OSError:
            pass
            # print("Server: ", e)
            # print("Server: Tentativa de fechar um socket não-conectado!")
        self.closed = True

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
            try:
                client, addr = self.server.accept()
                addr_str = "{}:{}".format(*addr)
                print("Servidor: Cliente conectado em ", addr_str)
                self.server.clients.append(client)
                self.new_client_signal.emit()
                t = threading.Thread(target=self.read_message, args=(client,))
                t.start()
            except OSError:
                self.finished.emit()
                break

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        uic.loadUi('ui/server.ui', self)
        self.server = Server()
        self.server_thread = ServerController(self.server)
        self.server_thread.message_signal.connect(self.update_chat_logging)
        self.server_thread.new_client_signal.connect(self.update_list_clients)
        self.server_thread.deleted_client_signal.connect(self.update_list_clients)
        self.server_thread.finished.connect(self.close)

    def closeEvent(self, event):
        if not self.server.closed:
            self.server.close()
        parent = self.parent()
        if not parent:
            sys.exit()

    def init_server(self):
        try:
            self.server.listen()
            msg = "Recebendo conexões em {}:{}".format(self.server.host,
                                                       self.server.port)
            self.statusBar().showMessage(msg)
            self.server_thread.start()
            self.show()
        except OSError:
            self.busy_port_error()

    def update_chat_logging(self):
        msg = self.server.messages.get()
        self.chat_text.insertPlainText(str(msg))
        self.chat_text.moveCursor(QtGui.QTextCursor.End)
        self.chat_text.ensureCursorVisible()

    def update_list_clients(self):
        self.clients_list.clear()
        for client in self.server.clients:
            addr = protocol.socket_dest_address(client)
            item = QtWidgets.QListWidgetItem(addr)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.clients_list.addItem(item)

    def busy_port_error(self):
        """Message box de erro: porta ocupada"""
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Uma merda enorme aconteceu!")
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.setText(f"A porta {self.server.port} está ocupada! Tente outra.")
        dlg.exec_()
        self.close()

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        main.init_server()
        sys.exit(app.exec_())


if __name__ == '__main__':
    ServerGUI.run()
