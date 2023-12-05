import clientInterface as I
import ClientConnection
import clientLogic as L
import time


def runClient(): 

    c = ClientConnection.ClientConnection()

    while True:
        
        n,p=I.logIn()
        c.sendMsg(L.sendLoginCredentials(n,L.generatePswHash(p)))
        serverResponse = L.decodeServerResponse(c.recvMsg())
        if serverResponse.__class__== list and serverResponse.__len__()==2: 
            clientType = serverResponse[0]
            clientId = serverResponse[1]
        else: clientType = None

        if clientType == None: I.wrongLogIn(serverResponse)
        elif clientType == 'clinician':
            while True:
                match I.clinician_mainMenu():
                    case 1: #Show all patients
                        c.sendMsg(L.clinician_requestPatientsList())
                        patientList = L.decodeServerResponse(c.recvMsg())
                        if patientList in (None,'huh'):
                            I.clinician_errorRetrievingInfoFromServer()
                        else:
                            I.clinician_showPatients(patientList)

                        input("Press to go back to menu...")

                    case 2:
                        c.sendMsg(L.clinician_requestPatientsList())
                        patientList = L.decodeServerResponse(c.recvMsg())
                        if patientList in (None, 'huh'):
                            I.clinician_errorRetrievingInfoFromServer()
                        else:
                            I.clinician_showPatients(patientList)
                            patientID = I.clinician_selectOption(patientList)
                            c.sendMsg(L.clinician_requestPatientReports(patientID))
                            patientReports = L.decodeServerResponse(c.recvMsg())
                            if patientReports in (None,'huh'):
                                I.clinician_errorRetrievingInfoFromServer()
                            else:
                                reports_available = I.clinician_showReports(patientReports)
                                if reports_available:
                                    reportID = I.clinician_selectOption(patientReports)
                                    I.clinician_showSelectedReport(patientReports, reportID)
                                    comment = I.clinician_addComment()
                                    if comment != None:
                                        c.sendMsg(L.clinician_addCommentToReport(reportID, comment))
                                        serverResponse = L.decodeServerResponse(c.recvMsg())
                                        if serverResponse.__class__ == tuple:
                                            I.printErrors(serverResponse[0])
                                        else:
                                            print(serverResponse)
                                input('Press intro to go back to the main menu...')
                                    
                    case 3:
                            c.sendMsg(L.clinician_requestPatientsList())
                            patientList = L.decodeServerResponse(c.recvMsg())
                            if patientList in (None, 'huh'):
                                I.clinician_errorRetrievingInfoFromServer()
                            else:
                                I.clinician_showPatients(patientList)
                                patientID = I.clinician_selectOption(patientList)
                                c.sendMsg(L.clinician_requestPatientReports(patientID))
                                patientReports = L.decodeServerResponse(c.recvMsg())
                                if patientReports in (None, 'huh'):
                                    I.clinician_errorRetrievingInfoFromServer()
                                else:
                                    reports_available = I.clinician_showReports(patientReports)
                                    if reports_available:
                                        reportID = I.clinician_selectOption(patientReports)
                                        I.clinician_showSelectedReport(patientReports, reportID)
                                    input('Press intro to go back to the main menu...')

                    case 4:
                        c.logOut()
                        raise SystemExit

                
        
        elif clientType == 'admin':
            while True:
                match I.admin_mainMenu():
                    case 1: #Create user
                        while True:
                            username, psw, usertype = I.admin_addUser()
                            if username==None: break
                            psw = L.generatePswHash(psw)
                            c.sendMsg(L.admin_createUser(username,psw,usertype))
                            serverResponse=L.decodeServerResponse(c.recvMsg())
                            if serverResponse.__class__ == tuple: I.printErrors(serverResponse[0]) 
                            else: print(serverResponse)
                            input("Press enter to go back to menu...")
                            break
                    case 2: #Delete user
                        c.sendMsg(L.admin_showAllUsers())
                        serverResponse=L.decodeServerResponse(c.recvMsg())
                        if serverResponse.__class__ == list:

                            while True:
                                usrID=I.admin_selectUserForDeletion(serverResponse)
                                if(usrID==None): break
                                c.sendMsg(L.admin_deleteUser(usrID))
                                serverResponse=L.decodeServerResponse(c.recvMsg())
                                if serverResponse.__class__ == tuple: I.printErrors(serverResponse[0])
                                else: print(serverResponse)
                                input("Press enter to go back to menu...")
                                break
                        elif serverResponse.__class__ == tuple: I.printErrors(serverResponse[0])
                        else:
                            input("Something went wrong. Press intro to go back to main menu...")
                    case 3: #Shutdown server
                        c.sendMsg(L.admin_shutdown())
                        serverResponse=L.decodeServerResponse(c.recvMsg())
                        if serverResponse.__class__ == tuple:
                            I.printErrors(serverResponse[0])
                        else:
                            print(serverResponse)
                            c.logOut()
                            raise SystemExit
                        input("Press enter to continue...")
                    case 4: #Log out
                        c.logOut()
                        raise SystemExit
                    case _: I.wrongOption()
        else: #its a patient, no more choices
            while True:
                match I.patient_mainMenu():
                    case 1:
                        while True:
                            patientSymptomsAndComments=I.patient_askForSymptoms()
                            if I.patient_askForParameters():
                                params=L.patient_connectToBitalino(I.patient_askForBitalinoMAC())
                                while True:
                                    if params==None:
                                        I.patient_bitalinoError()
                                        break
                                    c.sendMsg(L.patient_sendReport(patientSymptomsAndComments, clientId, params))
                                    serverResponse=L.decodeServerResponse(c.recvMsg())
                                    time.sleep(5)

                            else:
                                c.sendMsg(L.patient_sendReport(patientSymptomsAndComments, clientId))
                                serverResponse=L.decodeServerResponse(c.recvMsg())
                            if serverResponse.__class__ == tuple: I.patient_errorWithParams(serverResponse[0]) 
                            else: print(serverResponse)
                            break
                    case 2:
                        c.logOut()
                        raise SystemExit
                    case _: I.wrongOption()


if __name__ == "__main__": 
    runClient()
