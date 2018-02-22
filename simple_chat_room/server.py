from socket import *
import select
import queue


HOST = 'localhost'
PORT = 21357
BUFSIZE = 1024

message_queue = {}
fd_to_socket = {}
timeout = 10

def server_init(host, port):
    addr = (host, port)
    srv_socket = socket(AF_INET, SOCK_STREAM)
    srv_socket.bind(addr)
    srv_socket.listen(100)

    return srv_socket

def server_epoll_init(srv_socket):
    srv_epoll = select.epoll()
    srv_epoll.register(srv_socket.fileno(), select.EPOLLIN)
    fd_to_socket[srv_socket.fileno()] = srv_socket

    return srv_epoll

def server_epoll_run(srv_socket, srv_epoll):
    events = srv_epoll.poll(timeout)
    if not events:
        print("srv_epoll is timeout, requery")
        return
    for fd, event in events:
        e_socket = fd_to_socket[fd]
        if event & select.EPOLLIN:
            if e_socket == srv_socket:
                connection, address = srv_socket.accept()
                srv_epoll.register(connection.fileno(), select.EPOLLIN)
                fd_to_socket[connection.fileno()] = connection
                message_queue[connection] = queue.Queue()
            else:
                data = e_socket.recv(BUFSIZE)
                message_queue[e_socket].put(data)
                srv_epoll.modify(fd, select.EPOLLOUT)
        elif event & select.EPOLLOUT:
            try:
                msg = message_queue[e_socket].get_nowait()
            except queue.Empty:
                print("Empty queue")
                srv_epoll.modify(fd, select.EPOLLIN)
            else:
                for socket in fd_to_socket.values():
                    if socket != srv_socket:
                        socket.send(msg)
                    # e_socket.send(msg)

                # for e_fd in fd_to_socket:
                    # fd_to_socket[e_fd].send(msg)
                # e_socket.send(msg)
        elif event & select.EPOLLHUP:
            srv_epoll.unregister(fd)
            fd_to_socket[fd].close()
            del fd_to_socket[fd]

def server_close(s_socket, s_epoll):
    s_epoll.unregister(s_socket.fileno())
    s_epoll.close()
    s_socket.close()

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
                    for e_fd in self.fd_to_socket:
                        self.fd_to_socket[e_fd].send(msg)
                    # e_socket.send(msg)
            elif event & select.EPOLLHUP:
                self.srv_epoll.unregister(fd)
                self.fd_to_socket[fd].close()
                del self.fd_to_socket[fd]


    def chat_close(self):
        self.epoll.unregister(self.socket.fileno())
        self.epoll.close()
        self.socket.close()


if __name__ == "__main__":
    srv_socket = server_init(HOST, PORT)
    srv_epoll = server_epoll_init(srv_socket)

    while True:
        server_epoll_run(srv_socket, srv_epoll)

    server_close(srv_socket, srv_epoll)

