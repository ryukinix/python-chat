# coding: utf-8

import socket
import queue
import threading
import sys

import protocol

if sys.version_info >= (3, 7):
    from dataclasses import dataclass
    @dataclass
    class NamedSocket:
        socket: socket.socket
        name: str
else:
    class NamedSocket:
        def __init__(self, socket, name):
            self.socket = socket
            self.name = name


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


class ServerController(threading.Thread):

    """Classe de interface para controlar o Servidor"""

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        """Aceita conexões externas e dispara threads para leitura de mensagens"""
        threads = []
        print("Servidor: Thread de leitura de clientes inicializada!")
        while True:
            try:
                client, addr = self.server.accept()
                addr_str = "{}:{}".format(*addr)
                print("Servidor: Cliente conectado em ", addr_str)
                c = NamedSocket(client, None)
                self.server.clients.append(c)
                t = threading.Thread(target=self.read_message, args=(c,))
                t.start()
                threads.append(t)
            except OSError:
                break
        for t in threads:
            t.join()

    def read_message(self, client):
        """Lê mensagens do cliente e coloca na fila Server.messages"""
        addr = protocol.socket_dest_address(client.socket)
        print("Servidor: Nova thread disparada para o cliente: ", addr)
        while True:
            try:
                msg = protocol.Message.receive(client.socket)
                if client.name != msg.client_name:
                    client.name = msg.client_name
                self.server.messages.put(msg)
                self.server.send_broadcast(msg)
            except protocol.ClientClosedError:
                addr = protocol.socket_dest_address(client.socket)
                client_id = '{}@{}'.format(client.name, addr)
                print('Servidor: Cliente fechou a conexão: ', client_id)
                break
            except protocol.InvalidRequestError:
                addr = protocol.socket_dest_address(client.socket)
                client_id ='{}@{}'.format(client.name, addr)
                print('Servidor: Cliente mandou requisição inválida: ', client_id)
                break
        client.socket.close()
        self.server.clients.remove(client)


def main():
    server = Server()
    server.listen()
    controller = ServerController(server)
    try:
        print("Servidor iniciando...")
        controller.start()
        controller.join()
    except KeyboardInterrupt:
        print("\nServidor: servidor finalizado com Ctrl-C.")
    finally:
        server.close_clients()
        server.shutdown()
        server.close()


if __name__ == '__main__':
    main()
