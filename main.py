import sys

import client
import server
import protocol


from PyQt5 import QtWidgets
from PyQt5 import uic


class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.client_button.clicked.connect(self.open_client)
        self.server_button.clicked.connect(self.open_server)
        self.host_text.setText(protocol.HOST)
        self.port_text.setText(str(protocol.PORT))

    def update_host_port(self):
        protocol.HOST = self.host_text.text()
        protocol.PORT = int(self.port_text.text())

    def open_server(self):
        self.update_host_port()
        s = server.ServerGUI(parent=self)
        s.init_server()

    def open_client(self):
        self.update_host_port()
        c = client.ClientGUI(parent=self)
        c.init_client()

    @classmethod
    def run(cls):
        app = QtWidgets.QApplication(sys.argv)
        main = cls()
        main.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    MainGUI.run()
