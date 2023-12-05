import socket

def sndMsg(m:bytes, s:socket.socket):
    s.sendall(b'!sizeof:'+str(m.__sizeof__()).encode('utf8')+b':end!')
    if s.recv(1024) == b'ack':
        s.sendall(m)
        return 0
    else:
        return -1

def rcvMsg(s:socket.socket) -> bytes:
    i=s.recv(1024)

    if(i!=b''):i=i.split(b':')
    else: return b'DedSock'
    if(i.__class__!=list):return b'WrongFormat'
    if(i.__len__()!=3):return None
    if(i[0]!=b'!sizeof'):return b'WrongFormat'
    if(i[2]!=b'end!'):
        i2=10
        while i2!=0:
            if(s.recv(1)==b''): return b'DedSock'
            if(s.recv(1)!=b'!'):--i2
            else: break
            if(i==0): return b'WrongFormat'

    s.sendall(b'ack')

    fBytes=b''
    while True:
        rBytes=s.recv(1024)
        if(rBytes==b''): return b'DedSock'
        fBytes+=rBytes
        if(fBytes.__sizeof__()==int(i[1].decode('utf8'))): return fBytes
