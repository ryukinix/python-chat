import protocol
import socket
from datetime import datetime


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
        return self.socket.connect((self.host, self.port))

    def send_message(self, message, subject=None):
        m = protocol.Message(
            self.name,
            subject,
            message,
            datetime.now().strftime("%x %X")
        )
        return self.socket.send(m.to_string())


if __name__ == '__main__':
    c = Client()
    c.connect()
    print("Cliente conectado a {}:{}".format(c.host, c.port))
    c.send_message("Hey!")
    c.socket.close()
