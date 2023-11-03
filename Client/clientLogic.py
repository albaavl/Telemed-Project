import hashlib, json, pickle
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
        if response['control'] in ('success','error'): return response['content']
        else:return None
    except Exception: return None

#Patient Only    

def patient_connectToBitalino(mac:str) -> (list,False):
    '''Returns a `list` with all data received from the Bitalino, data is stored as a `str`"(timestamp,sample)"'''

    # Start the Java Virtual Machine (JVM)
    jpype.startJVM(jpype.getDefaultJVMPath())

    # Load the Java class
    bitalino = jpype.JClass('bitalinocutre')

    data=bitalino.dothethingy(mac,10)
    print(data)
    # Shutdown the JVM
    jpype.shutdownJVM()


    data=list()
    return data
    

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

def clinician_addComments(reportID:int, comments:str):
    return json.dumps({'control':'add_comments','content':[reportID,comments]}).encode('utf8')

#Admin only

def admin_createUser(name:str, psw:bytes, type:int):
    userData=(name,psw,type)    
    return pickle.dumps({'control':'add_user','content':userData})

def admin_showAllUsers():
    return json.dumps({'control':'show_all_users'}).encode('utf8')

def admin_deleteUser(userID:int):
    return json.dumps({'control':'delete_user','content':userID}).encode('utf8')