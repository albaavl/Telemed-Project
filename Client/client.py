import clientInterface as I
import ClientConnection
import clientLogic as L


def runClient(): 

    c = ClientConnection.ClientConnection()

    while True:
        try:
            n,p=I.logIn()
            c.sendMsg(L.sendLoginCredentials(n,L.generatePswHash(p)))
            clientType = L.decodeServerResponse(c.recvMsg(2048))
            if clientType in (None, 'wrongUserPassword'): I.wrongLogIn()
            elif clientType == 'clinician':
                pass
                #TODO MENU CLINICIAN
            elif clientType == 'admin':
                while True:
                    match I.admin_mainMenu():
                        case 1: #Create user
                            username, psw, usertype = I.admin_addUser()
                            psw = L.generatePswHash(psw)
                            c.sendMsg(L.admin_createUser(username,psw,usertype))
                            serverResponse=L.decodeServerResponse(c.recvMsg(2048))
                            if serverResponse in (None,'huh'): I.admin_failedUserCreation() #TODO replace placeholder error
                        case 2: #Delete user
                            c.sendMsg(L.admin_showAllUsers())
                            #TODO Show all users
                            while True:
                                usrID=I.admin_selectUser()
                                #TODO check if the user is valid
                                c.sendMsg(L.admin_deleteUser(usrID))
                                break
                            serverResponse=L.decodeServerResponse(c.recvMsg(2048))
                            if serverResponse in (None,'huh'): I.admin_failedUserCreation() #TODO replace placeholder error
                        case 3: #Log out
                            c.logOut()
                            raise SystemExit
                        case _: I.wrongOption()
            else: #its a patient, no more choices
                while True:
                    match I.patient_mainMenu():
                        case 1:
                            symptoms=I.patient_askForSymptoms()
                            if I.patient_askForParameters():
                                L.patient_connectToBitalino(I.patient_askForBitalinoMAC())
                                params=None
                                #TODO añadir control de error si no hay conexion correcta y guardar datos bitalino
                                c.sendMsg(L.generateParamsQuery(symptoms,params)) 
                            else: c.sendMsg(L.generateParamsQuery(symptoms)) 
                            if L.decodeQuery(c.recvMsg(2048)) in (None,'error?????'): I.patient_errorWithParams() #TODO replace placeholder error
                            else: I.success()
                        case 2:
                            c.logOut()
                            raise SystemExit
                        case _: I.wrongOption()

        except Exception : pass

if __name__ == "__main__": 
    runClient()
