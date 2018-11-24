# coding: utf-8

import json

HOST = '127.0.0.1'
PORT = 3131


class Message:

    """Protocolo compartilhado de mensagem cliente-servidor.

    Antes de enviar uma mensagem pelo Socket TCP é necessário
    converter todo o conteúdo em bytes codificada de tal
    maneira capaz de separá-la em diferentes atributos. A notação
    escolhida é o JSON (JavaScript Object Notation), muito similar ao
    tipo de dados dicionário em Python.

    {
       'client_name': 'str',
       'subject': 'str'
       'message': 'str',
       'date': 'str'
    }

    A finalização é feita por uma quebra de linha
    """

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

    def to_string(self) -> bytes:
        """Transforma a mensagem numa codificação JSON e então em bytes"""
        attrs = vars(self)
        json_string = json.dumps(attrs, ensure_ascii=False) + '\n'
        json_encoded = json_string.encode(Message.encoding)
        json_bytes = bytes(json_encoded)
        return json_bytes

    @classmethod
    def from_string(cls, message: bytes):
        """Transforma uma string em uma instância de Message"""
        dic = json.loads(message.decode(Message.encoding))
        return cls(dic['client_name'],
                   dic['subject'],
                   dic['message'],
                   dic['date'])
