import socket


class ClientConnection:
    '''Class containing client socket, any connection to server should be done through this class.'''

    def __init__(self,servIp:str|None='172.20.10.3',servPort:int|None=1111):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((servIp,servPort))
    
    def sendMsg(self,msg:bytes):
        '''Sends the provided bytes to the server'''
        print(msg)
        self.socket.send(msg)

    def recvMsg(self,buffSize:int):
        '''Returns bytes received from server'''

        fBytes=b''
        while True:
            rBytes=self.socket.recv(buffSize)
            fBytes+=rBytes
            if(len(rBytes)<buffSize): return fBytes
        

    def logOut(self):
        '''Close socket connection.'''
        self.socket.close()
