import socket


class ClientConnection:

    def __init__(self,servIp:str|None='127.0.0.1',servPort:int|None=1111):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((servIp,servPort))
    
    def sendMsg(self,msg:bytes):
        self.socket.send(msg)

    def recvMsg(self,buffSize:int):
        return self.socket.recv(buffSize)

    def logOut(self):
        self.socket.close()
