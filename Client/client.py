import clientInterface as I
import ClientConnection
import clientLogic as L


def runClient(): 

    c = ClientConnection.ClientConnection()

    while True:
        try:
            n,p=I.logIn()
            c.sendMsg(L.generateLogInQuery(n,L.generatePswHash(p)))
            if L.decodeQuery(c.recvMsg(2048)) in (None, 'wrongUserPassword'): I.wrongLogIn()
            else:   
                while True:
                    match I.mainMenu():
                        case 1:
                            symptoms=I.askForSymptoms()
                            if I.askForParameters():
                                L.connectToBitalino(I.askForBitalinoMAC())
                                params=None
                                #TODO añadir control de error si no hay conexion correcta
                                c.sendMsg(L.generateParamsQuery(symptoms,params)) #TODO enviar la info (con o sin params)
                            else: c.sendMsg(L.generateParamsQuery(symptoms)) 
                            if L.decodeQuery(c.recvMsg(2048)) in (None,'error?????'): I.errorWithParams()
                            else: I.success()
                        case 2:
                            c.logOut()
                            raise SystemExit
                        case _: I.wrongOption()

        except Exception : pass

if __name__ == "__main__": 
    runClient()
