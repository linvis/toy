# -*- coding: utf-8 -*-
# Pw @ 2018-01-31 21:31:54


from socket import *


HOST = 'localhost'
PORT = 21356
BUFSIZE = 1024

class chat_client:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)

    def chat_connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.addr)

    def chat_send(self, data):
        if not data:
            print("data to send is none")
        else:
            self.socket.send(data.encode('utf-8'))

    def chat_recv(self):
        self.recv_data = self.socket.recv(BUFSIZE)
        print(self.recv_data.decode('utf-8'))

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    client = chat_client()
    client.chat_connect()
    while(1):
        data = input('> ')
        client.chat_send(data)
        client.chat_recv()

    client.chat_close()




