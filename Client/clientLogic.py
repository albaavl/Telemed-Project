import hashlib, json, pickle, os, threading
import socket
# import jpype1
# from pylsl import StreamInlet, resolve_stream


def generatePswHash(password:str):
    hashgen = hashlib.sha512()
    hashgen.update(password.encode('utf8'))
    return hashgen.digest()

def sendLoginCredentials(usr:str,psw:bytes):
    return pickle.dumps({'control':'login','content':[usr,psw]}) 

def decodeServerResponse(query:bytes):
    '''Return `content` AKA the response value, or  `None` if the response has invalid format'''
    try:
        response=json.loads(query)
        if not response: return None
        if response['control'] == 'success': return response['content']
        elif response['control'] == 'error': return (response['content'],)
        else:return None
    except Exception: return None

#Patient Only    

def patient_connectToBitalino(mac:str="20:16:07:18:17:85", iterations:str="10") -> (list):

    data=list()
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    chapuza = threading.Thread(target=patient_chapuza, args=(mac,iterations), daemon=True)
    chapuza.start()

    sck.connect(('127.0.0.1',50500))

    while(True):
        dataIn = sck.recv(2048)
        if dataIn== b'':    break
        stringIn=dataIn.decode('utf8')
        stringIn=stringIn.split(" ")
        
        for string in stringIn:
            data.append(string)

    sck.close()

    return data

def patient_chapuza(mac:str, iterations:str):
    os.system("java -jar --enable-preview Client/bitalino.jar "+mac+" "+iterations)


def patient_sendParams(patientInput:str, clientId:int, params:list=None):
    '''`Content:` list [patientInput(String),params(list)]'''    
    inputData=[clientId,patientInput,]
    if params != None: inputData.append(params)
    return json.dumps({'control':'new_report','content':inputData}).encode('utf8')

#Clinician only

def clinician_requestPatientsList():
    return json.dumps({'control':'show_patients'}).encode('utf8')

def clinician_requestPatientReports(patientID:int):
    return json.dumps({'control':'show_reports','content':patientID}).encode('utf8')

def clinician_addCommentToReport(reportID:int, comments:str):
    return json.dumps({'control':'add_comments','content':[reportID,comments]}).encode('utf8')

#Admin only

def admin_createUser(name:str, psw:bytes, userType:str):
    userData=(name,psw,userType)    
    return pickle.dumps({'control':'add_user','content':userData})

def admin_showAllUsers():
    return json.dumps({'control':'show_users'}).encode('utf8')

def admin_deleteUser(userID:int=999):
    return json.dumps({'control':'delete_user','content':userID}).encode('utf8')