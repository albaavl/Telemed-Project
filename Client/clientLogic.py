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

# def patient_connectToBitalino(mac:str) -> (list,False):
#     '''Returns a `list` with all data received from the Bitalino, data is stored as a `str`"(timestamp,sample)"'''
#     os_stream=resolve_stream("type", mac) #TODO CHANGE TYPE FOR THE ACTUAL DATA TYPE WE'RE OBTAINING
#     if os_stream is None: return False
#     inlet=StreamInlet(os_stream[0])
#     data=[]
#     while True:
#         samples,timestamp= inlet.pull_sample()
#         if (samples,timestamp) is (None,None): break
#         data.append("("+timestamp+","+samples+")")
#     return data
    

def patient_sendParams(patientInput:str, params:list=None):
    '''`Content:` list [patientInput(String),params(list)]'''    
    inputData=[patientInput,]
    if params != None: inputData.append(params)
    return json.dumps({'control':'new_report','content':inputData})

#Clinician only

def clinician_requestPatientsList():
    return json.dumps({'control':'show_patients'})

def clinician_requestPatientReports(patientID:int):
    return json.dumps({'control':'show_reports','content':patientID})

#Admin only

def admin_createUser(name:str, psw:bytes, type:int):
    userData=(name,psw,type)
    return pickle.dumps({'control':'add_user','content':userData})

def admin_showAllUsers():
    return json.dumps({'control':'show_all_users'})

def admin_deleteUser(userID:int):
    return json.dumps({'control':'delete_user','content':userID})