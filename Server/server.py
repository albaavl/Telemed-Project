import socket, select, pickle

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
            for clientSocket in r_socket:
                if clientSocket == self.sockets[0]:
                    self.accept_client()
                else:
                    self.read_message(clientSocket)

    def accept_client(self):
        s_client, direction_client = self.sockets[0].accept()
        self.sockets.append(s_client)
        print("Connection opened")
        print(direction_client)

    def read_message(self, csocket):
        message = csocket.recv(1024)
        if not message:
            self.disconnectClient(csocket)
        else:
            dic_message = pickle.loads(message)
            print(dic_message)
            if not dic_message:
                print('Disconnected')
                self.disconnectingClient(csocket)
            else:
                print('Message received')
                self.decode_message(dic_message,csocket)

    def decode_message(self,dic_message,csocket):
        possible_controls = ['new_report','show_patients','show_reports','add_comments','add_user','delete_user','login']
        if dic_message['control'] not in possible_controls:
            csocket.send(pickle.dumps({'control': 'error', 'content':'Error: format not understood'}))
        elif dic_message['control'] == 'new_report':
            #TODO add report to database and error control
            print('adding new report')
            csocket.send(pickle.dumps({'control': 'success', 'content': 'Success: report added to database'}))
        elif dic_message['control'] == 'show_patients':
            #TODO database
