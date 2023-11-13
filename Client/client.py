import clientInterface as I
import ClientConnection
import clientLogic as L


def runClient(): 

    c = ClientConnection.ClientConnection()

    while True:
        try:
            n,p=I.logIn()
            c.sendMsg(L.sendLoginCredentials(n,L.generatePswHash(p)))
            clientType,clientId = L.decodeServerResponse(c.recvMsg(2048))
            if clientType in (None, 'wrongUserPassword'): I.wrongLogIn()
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
                                if patientReports in (None,'huh'):
                                    I.clinician_errorWithPatients()
                                else:
                                    report = I.clinician_showPatientReports(patientReports)
                                    I.showSelectedReport(report)
                        case 2: #Add comment to a report
                            #HAY UNA COCHINADA DE CODIGO REDUNDANTE, QUEDA PENDIENTE HACER UN REFACTOR
                            # Y UBICARME RESPECTO A LA ESTRUCTURA DEL REPORT

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
                                    I.showSelectedReport(report)
                                    comment = I.clinician_addComment()
                                    c.sendMsg(L.clinician_addCommentToReport(report.id,comment))
                                    serverResponse=L.decodeServerResponse(c.recvMsg(2048))
                                    if serverResponse in (None,'huh'): I.clinician_failedCommentCreation()
                                 #TODO RESTO DEL MENU CLINICIAN
                
            
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
                            serverResponse=L.decodeServerResponse(c.recvMsg(8192))
                            print(serverResponse)
                            # while True:
                            #     usrID=I.admin_selectUser()
                            #     #TODO check if the user is valid
                            #     c.sendMsg(L.admin_deleteUser(usrID))
                            #     break
                            # serverResponse=L.decodeServerResponse(c.recvMsg(2048))
                            # if serverResponse in (None,'huh'): I.admin_failedUserCreation() #TODO replace placeholder error
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
                                params=L.patient_connectToBitalino(I.patient_askForBitalinoMAC())
                                
                                #TODO añadir control de error si no hay conexion correcta y guardar datos bitalino
                                c.sendMsg(L.patient_sendParams(symptoms,params,clientId)) 
                            else:
                                c.sendMsg(L.patient_sendParams(symptoms,clientId)) 
                            if L.decodeServerResponse(c.recvMsg(2048)) in (None,'error?????'): I.patient_errorWithParams() #TODO replace placeholder error
                            else: I.success()
                        case 2:
                            c.logOut()
                            raise SystemExit
                        case _: I.wrongOption()

        except Exception : pass

if __name__ == "__main__": 
    runClient()
