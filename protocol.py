# coding: utf-8

import json

HOST = '127.0.0.1'
PORT = 9999


class ClientClosedError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class Message:

    '''Protocolo compartilhado de mensagem cliente-servidor.

    Antes de enviar uma mensagem pelo Socket TCP é necessário
    converter todo o conteúdo em bytes codificada de tal
    maneira capaz de separá-la em diferentes atributos. A notação
    escolhida é o JSON (JavaScript Object Notation), muito similar ao
    tipo de dados dicionário em Python. Adicionalmente é enviado
    um header também com o tamanho da mensagem.

    Content-length: int
    {
       "client_name": "str",
       "subject": "str",
       "message": "str",
       "date": "str"
    }
   '''

    encoding = 'utf-8'

    def __init__(self,
                 client_name: str,
                 subject: str,
                 message: str,
                 date: str):
        self.client_name = client_name
        self.subject = subject
        self.message = message
        self.date = date

    def __repr__(self):
        attrs = ', '.join(['{}={!r}'.format(k, v)
                           for k, v in vars(self).items()])
        return f'Message({attrs})'

    def __str__(self):
        msg = ('-\n'
               'Cliente: {client_name}\tData: {date}\n'
               'Assunto: {subject}\n'
               'Mensagem: {message}\n'
               '-\n')
        return msg.format_map(vars(self))

    def to_bytes(self) -> bytes:
        """Transforma a mensagem numa codificação JSON e então em bytes.
        """
        attrs = vars(self)
        json_string = json.dumps(attrs, ensure_ascii=False) + '\n'
        json_encoded = json_string.encode(Message.encoding)
        json_bytes = bytes(json_encoded)
        return json_bytes

    @classmethod
    def from_bytes(cls, message: bytes):
        """Transforma uma string em uma instância de Message"""
        dic = json.loads(message.decode(cls.encoding))
        return cls(dic['client_name'],
                   dic['subject'],
                   dic['message'],
                   dic['date'])

    @classmethod
    def receive(cls, socket):
        """Recebe uma mensagem e decodifica a partir de um socket."""
        header = cls.readline(socket)
        try:
            attr, value = header.split(':')
            if attr != 'Content-length':
                raise InvalidRequestError("Invalid header: expected Content-length, got " + attr)
            length = int(value)
            msg = socket.recv(length)
            return cls.from_bytes(msg)
        except Exception as e:
            print("protocol.Message.receive exception: ", e)
            raise InvalidRequestError("Invalid Request!")

    def send(self, socket):
        """Envia uma mensagem codificada para um determinado socket"""
        msg_bytes = self.to_bytes()
        content_length = 'Content-length:{}\n'.format(len(msg_bytes))
        content_length_bytes = content_length.encode(self.encoding)
        socket.sendall(content_length_bytes + msg_bytes)

    @staticmethod
    def readline(socket):
        """Lê os caracteres de um socket até a quebra de linha"""
        msg = bytes()
        while True:
            try:
                c = socket.recv(1)
            except OSError:
                raise ClientClosedError('Cliente morreu inesperadamente!')
            if c == b'\n':
                break
            elif c == b'':  # quando uma conexão é fechada, recv() retorna um byte vazio
                raise ClientClosedError('Cliente fechou a conexão!')
            msg += c
        return msg.decode(Message.encoding)


def socket_source_address(socket):
    return ':'.join(map(str, socket.getsockname()))


def socket_dest_address(socket):
    return ':'.join(map(str, socket.getpeername()))
