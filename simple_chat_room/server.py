from socket import *
import select
import queue


HOST = 'localhost'
PORT = 21356
BUFSIZE = 1024

class chat_server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)

    def chat_listen(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.addr)
        self.socket.listen(100)

    def chat_recv(self):
        print("wait for connected")
        self.client_socket, self.client_addr = self.socket.accept()
        print("connected")
        while True:
            data = self.client_socket.recv(BUFSIZE)
            if not data:
                pass
            else:
                self.client_socket.send(data)

    def chat_epoll_init(self):
        self.srv_epoll = select.epoll()
        self.srv_epoll.register(self.socket.fileno(), select.EPOLLIN)
        self.message_queue = {}
        self.timeout = 10
        self.fd_to_socket = {self.socket.fileno():self.socket}


    def chat_epoll_run(self):
        self.events = self.srv_epoll.poll(self.timeout)
        if not self.events:
            print("srv_epoll is timeout, requery")
            return
        for fd, event in self.events:
            e_socket = self.fd_to_socket[fd]
            if event & select.EPOLLIN:
                if e_socket == self.socket:
                    connection, address = server.socket.accept()
                    self.srv_epoll.register(connection.fileno(), select.EPOLLIN)
                    self.fd_to_socket[connection.fileno()] = connection
                    self.message_queue[connection] = queue.Queue()
                else:
                    data = e_socket.recv(BUFSIZE)
                    self.message_queue[e_socket].put(data)
                    self.srv_epoll.modify(fd, select.EPOLLOUT)
            elif event & select.EPOLLOUT:
                try:
                    msg = self.message_queue[e_socket].get_nowait()
                except queue.Empty:
                    print("Empty queue")
                    self.srv_epoll.modify(fd, select.EPOLLIN)
                else:
                    e_socket.send(msg)
            elif event & select.EPOLLHUP:
                self.srv_epoll.unregister(fd)
                self.fd_to_socket[fd].close()
                del self.fd_to_socket[fd]


    def chat_close(self):
        self.epoll.unregister(self.socket.fileno())
        self.epoll.close()
        self.socket.close()


if __name__ == "__main__":
    server = chat_server()
    server.chat_listen()
    server.chat_epoll_init()

    while True:
        server.chat_epoll_run()

    self.chat_close()

