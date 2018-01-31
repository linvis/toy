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

    def connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.addr)

    def send(self, data):
        if not data:
            print("data to send is none")
        else:
            self.socket.send(data)

    def recv(self):
        self.recv_data = self.socket.recv(BUFSIZE)
        print(self.recv_data)

    def close(self):
        self.socket.close()


if __name__ == "main":
    client = chat_client()
    client.connect()
    while(1):
        data = input()
        client.send(data)
        client.recv()

    client.close()




