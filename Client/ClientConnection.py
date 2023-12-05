import socket


class ClientConnection:
    '''Class containing client socket, any connection to server should be done through this class.'''

    def __init__(self,servIp:str|None='192.168.1.37',servPort:int|None=1111):
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((servIp,servPort)) 
    
    def sendMsg(self,msg:bytes):
        '''Sends the provided bytes to the server'''
        self.socket.sendall(b'!sizeof:'+str(msg.__sizeof__()).encode('utf8')+b':end!')
        if self.socket.recv(1024) == b'ack':
            self.socket.sendall(msg)
            return 0
        else:
            return -1

    def recvMsg(self):
        '''Returns bytes received from server'''
        try:
            inB=self.socket.recv(1024)
            if(inB!=b''):inB=inB.split(b':')
            else: return None
            if(inB.__class__!=list):return b'WrongFormat'
            if(inB.__len__()!=3):return b'DedSock'
            if(inB[0]!=b'!sizeof'):return b'WrongFormat'
            if(inB[2]!=b'end!'):
                i=10
                while i!=0:
                    if(self.socket.recv(1)==b''): return b'DedSock'
                    if(self.socket.recv(1)!=b'!'):--i
                    else: break
                    if(i==0): return b'WrongFormat'

            self.socket.sendall(b'ack')

            fBytes=b''
            while True:
                rBytes=self.socket.recv(16384)
                if(rBytes==b''): return b'DedSock'
                fBytes+=rBytes
                if(fBytes.__sizeof__()==int(inB[1].decode('utf8'))): return fBytes
        except ConnectionResetError:return b'DedSock'

    def logOut(self):
        '''Close socket connection.'''
        self.socket.close()
