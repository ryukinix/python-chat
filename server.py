# coding: utf-8

import socket
import sys
import queue
import threading

# PyQt5 imports
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from dataclasses import dataclass

import protocol
import gui.server

@dataclass
class NamedSocket:
    socket: socket.socket
    name: str


class Server(object):

    """Servidor do sistema de chat"""

    def __init__(self):
        self.host = protocol.HOST
        self.port = protocol.PORT
        self.socket = socket.socket(
            socket.AF_INET,      # IPV4
            socket.SOCK_STREAM   # TCP
        )
        self.socket.setsockopt(  # socket magic options
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        self.clients = []              # socket de clientes no sistema
        self.messages = queue.Queue()  # fila de mensagens
        self.closed = False

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def accept(self):
        return self.socket.accept()

    def close_clients(self):
        for client in self.clients:
            client.socket.shutdown(socket.SHUT_RDWR)

    def shutdown(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    def close(self):
        print("Servidor: Servidor sendo fechado!")
        try:
            self.socket.close()
        except OSError:
            pass
            # print("Server: ", e) print("Server: Tentativa de fechar
            # um socket não-conectado!")
        self.closed = True

    def send_broadcast(self, message):
        for client in self.clients:
            message.send(client.socket)


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
        threads = []
        while True:
            try:
                client, addr = self.server.accept()
                addr_str = "{}:{}".format(*addr)
                print("Servidor: Cliente conectado em ", addr_str)
                c = NamedSocket(client, None)
                self.server.clients.append(c)
                self.new_client_signal.emit()
                t = threading.Thread(target=self.read_message, args=(c,))
                t.start()
                threads.append(t)
            except OSError:
                break
        for t in threads:
            t.join()

    def read_message(self, client):
        """Lê mensagens do cliente e coloca na fila Server.messages"""
        while True:
            try:
                msg = protocol.Message.receive(client.socket)
                if client.name != msg.client_name:
                    client.name = msg.client_name
                    self.new_client_signal.emit()
                self.server.messages.put(msg)
                self.server.send_broadcast(msg)
                self.message_signal.emit()
            except protocol.ClientClosedError:
                addr = protocol.socket_dest_address(client.socket)
                client_id = '{}@{}'.format(client.name, addr)
                print('Servidor: Cliente fechou a conexão: ', client_id)
                self.server.clients.remove(client)
                client.socket.close()
                self.deleted_client_signal.emit()
                break


class ServerGUI(QtWidgets.QMainWindow):

    """Interface gráfica principal do sistema feita em Qt"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = gui.server.Ui_ServerWindow()
        self.ui.setupUi(self)
        self.server = Server()
        self.server_thread = ServerController(self.server)
        self.server_thread.message_signal.connect(self.update_chat_logging)
        self.server_thread.new_client_signal.connect(self.update_list_clients)
        self.server_thread.deleted_client_signal.connect(self.update_list_clients)

    def closeEvent(self, event):
        if not self.server.closed:
            self.server.close_clients()
            self.server.shutdown()
            self.server_thread.wait()
            self.server.close()
            del self.server.socket
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
        self.ui.chat_text.insertPlainText(str(msg))
        self.ui.chat_text.moveCursor(QtGui.QTextCursor.End)
        self.ui.chat_text.ensureCursorVisible()

    def update_list_clients(self):
        self.ui.clients_list.clear()
        for client in self.server.clients:
            client_id = protocol.socket_dest_address(client.socket)
            if client.name:
                client_id = client.name + '@' + client_id
            item = QtWidgets.QListWidgetItem(client_id)
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            self.ui.clients_list.addItem(item)

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
