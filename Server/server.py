import socket, select, pickle, json, databaseManager as db
from datetime import date

class myServer:
    def __init__(self, ip_port=("0.0.0.0",1111)):
        self.address = ip_port
        self.sockets = []
        self.dbManager = db.Manager()


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
            try: dic_message = json.loads(message)
            except UnicodeDecodeError: dic_message = pickle.loads(message)
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
            csocket.send(json.dumps({'control': 'error', 'content':'Error: format not understood'}).encode('utf8'))
        elif dic_message['control'] == 'new_report':
            #receives a list 1st element = symptoms and 2nd = bitalino
            content = dic_message['content']
            if len(content) < 3: #in case there is no bitalino reading in the report
                content.append(None)
            self.dbManager.new_report(content[0],content[1], content[2], date.today())
            print('adding new report')
            csocket.send(json.dumps({'control': 'success', 'content': 'Success: report added to database'}).encode('utf8'))
        elif dic_message['control'] == 'show_patients':
            patientList = self.dbManager.get_patients()
            print('getting patients from db')
            csocket.send(json.dumps({'control': 'success', 'content': patientList}).encode('utf8'))
        elif dic_message['control']=='show_reports':
            #the content of the dic is the user_id of the patient
            reports = self.dbManager.get_reports(dic_message['content'])
            print('getting reports from db')
            csocket.send(json.dumps({'control': 'success', 'content': reports}).encode('utf8'))
        elif dic_message['control'] == 'add_comments':
            #the content of the dic is the report_id
            self.dbManager.add_comments(dic_message['content'])
            print('adding comments to db')
            csocket.send(json.dumps({'control': 'success', 'content': 'New comments successfully added to the report'}).encode('utf8'))
        elif dic_message['control'] == 'add_user':
            username, password, userType = dic_message['content'][0],dic_message['content'][1], dic_message['content'][2]
            self.dbManager.createUser(username, password, userType)
            print('adding user to db')
            csocket.send(json.dumps({'control': 'success', 'content': 'New user successfully added'}).encode('utf8'))
        elif dic_message['control'] == 'delete_user':
            #the content of the dic is the user_id
            self.dbManager.deleteUser(dic_message['content'])
            print('Deleting user')
            csocket.send(json.dumps({'control': 'success', 'content': 'User deleted successfully'}).encode('utf8'))
        elif dic_message['control'] == 'login':
            #content = list -> first element is the username and the 2nd is the password
            userpass = dic_message['content']
            username = userpass[0]
            password = userpass[1]
            (userType,userId) = self.dbManager.checkUser(username, password)
            print('logging in new client')
            csocket.send(json.dumps({'control': 'success', 'content': (userType,userId)}).encode('utf8'))

    def disconnectClient(self, csocket):
       csocket.close()
       self.sockets.remove(csocket)
       print('Client out!')
       
if __name__ == "__main__": 
    try:
        server = myServer()
        server.startServer()
        server.listen()
    except: pass