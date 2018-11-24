import protocol
import socket


class Server(object):

    def __init__(self, host=protocol.HOST, port=protocol.PORT):
        self.host = host
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET,     # IPV4
            socket.SOCK_STREAM  # TCP
        )
        self.socket.bind((host, port))
        self.clients = []

    def listen(self):
        print(f"Socket listening in {self.host}:{self.port}")
        return self.socket.listen(5)

    def accept(self):
        return self.socket.accept()

    def read_message(self):
        pass

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    s = Server()
    s.listen()
    client, addr = s.accept()
    print("Cliente conectado: ", addr)
    client.close()
    s.close()
