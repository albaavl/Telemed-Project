import clientInterface as I
import ClientConnection
import clientLogic as L


def runClient(): 

    c = ClientConnection.ClientConnection()

    while True:
        # try:
            n,p=I.logIn()
            c.sendMsg(L.sendLoginCredentials(n,L.generatePswHash(p)))
            serverResponse = L.decodeServerResponse(c.recvMsg(2048))
            if serverResponse.__class__== list and serverResponse.__len__()==2: 
                clientType = serverResponse[0]
                clientId = serverResponse[1]
            else: clientType = None

            if clientType == None: I.wrongLogIn(serverResponse)
            elif clientType == 'clinician':
                while True:
                    match I.clinician_mainMenu():
                        case 1: #Show all patients and reports
                            c.sendMsg(L.clinician_requestPatientsList())
                            patientList = L.decodeServerResponse(c.recvMsg(2048))
                            if patientList in (None,'huh'):
                                I.clinician_errorWithPatients()
                            else:
                                '''Sends the position of the desired patient within the server's list of patients, and receives the patient's data'''
                                patientID = I.clinician_showPatients(patientList)
                                c.sendMsg(L.clinician_requestPatientReports(patientID))
                                patientReports = L.decodeServerResponse(c.recvMsg(2048))
                                # report = I.clinician_showPatientReports(patientReports)
                                # I.showSelectedReport(report)
                                
                                
                                I.showSelectedReport(report)
                                if patientReports in (None,'huh'):
                                    I.clinician_errorWithPatients()
                                else:
                                    
                                    report = I.clinician_showPatientReports(patientReports)
                                
                                    I.clinician_showSelectedReport(report)
                        case 2: 

                            c.sendMsg(L.clinician_requestPatientsList())
                            patientList = L.decodeServerResponse(c.recvMsg(2048))
                            if patientList in (None,'huh'):
                                I.clinician_errorWithPatients()
                            else:
                                '''Sends the position of the desired patient within the server's list of patients, and receives the patient's data'''
                                patientID = I.clinician_showPatients(patientList)
                                c.sendMsg(L.clinician_requestPatientReports(patientID))
                                patientReports = L.decodeServerResponse(c.recvMsg(2048))
                                if patientReports in (None,'huh'):
                                    I.clinician_errorWithPatients()
                                else:
                                    report = I.clinician_showPatientReports(patientReports)
                                    reportID =  report[0]
                                    I.clinician_showSelectedReport(report)
                                    comment = I.clinician_addComment()
                                    c.sendMsg(L.clinician_addCommentToReport(reportID,comment))
                                    serverResponse=L.decodeServerResponse(c.recvMsg(2048))
                                    if serverResponse in (None,'huh'): I.clinician_failedCommentCreation()
                                    else: I.success()
                    
            
            elif clientType == 'admin':
                while True:
                    match I.admin_mainMenu():
                        case 1: #Create user
                            username, psw, usertype = I.admin_addUser()
                            psw = L.generatePswHash(psw)
                            c.sendMsg(L.admin_createUser(username,psw,usertype))
                            serverResponse=L.decodeServerResponse(c.recvMsg(8192))
                            if serverResponse.__class__ == tuple: I.admin_failedUserCreation(serverResponse[0]) #TODO replace placeholder error
                        case 2: #Delete user
                            c.sendMsg(L.admin_showAllUsers())
                            serverResponse=L.decodeServerResponse(c.recvMsg(8192))
                            if serverResponse.__class__ == list:

                                while True:
                                    usrID=I.admin_selectUser(serverResponse)
                                    c.sendMsg(L.admin_deleteUser(usrID))
                                    break
                                if serverResponse.__class__ == tuple: I.admin_failedUserCreation() #TODO replace placeholder error
                                serverResponse=L.decodeServerResponse(c.recvMsg(8192))
                                print(serverResponse)
                                input("Press enter to go back to menu...")
                            else:
                                input("Something went wrong. Press intro to go back to main menu...")
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
                                params=L.patient_connectToBitalino()
                                c.sendMsg(L.patient_sendParams(symptoms, clientId, params))
                            else:
                                c.sendMsg(L.patient_sendParams(symptoms,clientId)) 
                                serverResponse=L.decodeServerResponse(c.recvMsg(8192))
                            if serverResponse.__class__ == tuple: I.patient_errorWithParams(serverResponse[0]) #TODO replace placeholder error
                            else: I.success()
                        case 2:
                            c.logOut()
                            raise SystemExit
                        case _: I.wrongOption()

        # except Exception : pass

if __name__ == "__main__": 
    runClient()
