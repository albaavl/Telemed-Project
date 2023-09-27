import socket, select

class myServer:
    def __init__(self, ip_port=("0.0.0.0",1111)):
        self.address = ip_port
        self.sockets = []

    def startServer(self):
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sockets.append(socketServer)
        self.sockets[0].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockets[0].bind(self.address)
        self.sockets[0].listen(5)
        print('Server up!')

    def listen(self):
        while True:
            r_socket, _, _ = select.select(self.sockets[:], [], [])
            for s in r_socket:
                if s == self.sockets[0]:
                    self.accept_client()
                else:

                    # self.read_message(s)

    def accept_client(self):
        s_client, direction_client = self.sockets[0].accept()
        self.sockets.append(s_client)
        print("Connection opened")

