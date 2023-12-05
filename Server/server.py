import socket, select, pickle, json, databaseManager as db
from datetime import date

class myServer:
    def __init__(self, ip_port=("0.0.0.0",1111)):
        self.address = ip_port
        self.sockets = []
        self.dbManager = db.Manager()


    def startServer(self):
        '''This function is used to turn on the server'''
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sockets.append(socketServer)
        self.sockets[0].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockets[0].bind(self.address)
        self.sockets[0].listen(5)
        
        print('Server up!')

    def closeServer(self):
        '''This function is used to turn off the server'''
        print('Server out!')
        self.disconnectClient(self.sockets[1])
        self.sockets[0].close()
        raise SystemExit

    def listen(self):
        '''This function is used to permanently listen from the main socket of the server to be able to accept new clients as well as receiving new messages from each of the sockets of the clients'''
        while True:
            r_socket, _, _ = select.select(self.sockets[:], [], [])
            for clientSocket in r_socket:
                if clientSocket == self.sockets[0]:
                    #this means that it is a new client as it is using the main socket of the server
                    self.accept_client()
                else:
                    self.read_message(clientSocket)

    def accept_client(self):
        '''This function is used to accept a new client, create a new socket to communicate with it and add it to the list of opened sockets'''
        s_client, direction_client = self.sockets[0].accept()
        self.sockets.append(s_client)
        print("Connection opened")
        print(direction_client)

    def disconnectClient(self, csocket):
        '''This function is used to disconnect a client'''
        csocket.close()
        self.sockets.remove(csocket)
        print('Client out!')

    def read_message(self, csocket):
        '''This function is used to receive messages from the sockets of the clients'''
        final_message = b''
        try:
            message = csocket.recv(8096)
        except ConnectionResetError:
            self.disconnectClient(csocket)
            return
        if len(message)<8096:
            final_message += message
        else:
            final_message += message
            while message:
                message = csocket.recv(8096)
                final_message += message
                if len(message)<8096:
                    break
        try: dic_message = json.loads(final_message)
        except UnicodeDecodeError: dic_message = pickle.loads(final_message)
        #this is done because the password as bytes cannot be read using a json so we employ the pickle class
        if not dic_message:
            print('Disconnected')
            self.disconnectClient(csocket)
        else:
            print('Message received')
            self.decode_message(dic_message, csocket)

    def decode_message(self,dic_message,csocket):
        '''This function is used to decode the instructions recieved from the clients and generate and send the appropiate response'''
        possible_controls = ['new_report','show_patients','show_reports', 'show_users','add_comments','add_user','delete_user','login', 'shut_down']
        try:
            if dic_message['control'] not in possible_controls:
                raise Exception('Error: format not understood')
            elif dic_message['control'] == 'new_report':
                #receives a list [patient_id, fatigue, dizziness, sweating, symptoms, parambitalino]
                content = dic_message['content']
                if len(content) < 6: #in case there is no bitalino reading in the report
                    content.append(None)
                self.dbManager.new_report(content[0],content[1], content[2], content[3], content[4], content[5], date.today())
                print('Adding new report')
                csocket.send(json.dumps({'control': 'success', 'content': 'Success: report added to database'}).encode('utf8'))
            elif dic_message['control'] == 'show_patients':
                patientList = self.dbManager.get_patients()
                print('Getting patients from db')
                csocket.send(json.dumps({'control': 'success', 'content': patientList}).encode('utf8'))
            elif dic_message['control'] == 'show_users':
                usersList = self.dbManager.get_users()
                print('Getting users from db')
                csocket.send(json.dumps({'control': 'success', 'content': usersList}).encode('utf8'))
            elif dic_message['control']=='show_reports':
                #the content of the dic is the user_id of the patient
                reports = self.dbManager.get_reports(dic_message['content'])
                print('Getting reports from db')
                csocket.send(json.dumps({'control': 'success', 'content': reports}).encode('utf8'))
            elif dic_message['control'] == 'add_comments':
                #the content of the dic is the report_id, comments to add
                self.dbManager.add_comments(dic_message['content'][0],dic_message['content'][1])
                print('Adding comments to db')
                csocket.send(json.dumps({'control': 'success', 'content': 'New comments successfully added to the report'}).encode('utf8'))
            elif dic_message['control'] == 'add_user':
                username, password, userType = dic_message['content'][0],dic_message['content'][1], dic_message['content'][2]
                self.dbManager.createUser(username, password, userType)
                print('Adding user to db')
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
                print('Logging in new client')
                csocket.send(json.dumps({'control': 'success', 'content': (userType,userId)}).encode('utf8'))
            elif dic_message['control'] == 'shut_down':
                #sockets list length is used to determined if only the listening socket of the server and the admin socket is connected
                if len(self.sockets) == 2:
                    csocket.send(json.dumps({'control': 'success', 'content': 'There are no other clients connected, shutting down the server, this action cannot be undone'}).encode('utf8'))
                    server.closeServer()
                else:
                    raise Exception('There are clients currently connected to the server, try again later')

        except Exception as e:
            print(e)
            csocket.send(json.dumps({'control': 'error', 'content': e.args}).encode('utf8'))



if __name__ == "__main__":
    server = myServer()
    server.startServer()
    while True:
        server.listen()

