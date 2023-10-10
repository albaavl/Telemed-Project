import hashlib, pickle
from pylsl import StreamInlet, resolve_stream


def generatePswHash(password:str):
    hashgen = hashlib.sha512()
    hashgen.update(password.encode('utf8'))
    return hashgen.digest()

def connectToBitalino(mac:str) -> (list,False):
    '''Returns a `list` with all data received from the Bitalino, data is stored as a `str`"(timestamp,sample)"'''
    os_stream=resolve_stream("type", mac)#TODO CHANGE TYPE FOR THE ACTUAL DATA TYPE WE'RE OBTAINING
    if os_stream is None: return False
    inlet=StreamInlet(os_stream[0])
    data=[]
    while True:
        samples,timestamp= inlet.pull_sample()
        if (samples,timestamp) is (None,None): break
        data.append("("+timestamp+","+samples+")")
    return data
    

def sendParams(patientInput:str, params:list=None):
    '''`Content:` list [patientInput(String),params(list)]'''    
    inputData=[patientInput,]
    if params != None: inputData.append(params)
    return pickle.dumps({'control':'new_report','content':inputData})

def sendLoginCredentials(usr:str,psw:bytes):
    return pickle.dumps({'control':'login','content':[usr,psw]}) 


def decodeServerResponse(query:bytes)->(str|None):
    '''Return `(str)content` AKA the response value, or  `None` if the response has invalid format'''
    try:
        response=pickle.loads(query)
        if not response: return None
        if response['control'] in ('success','error'): return response['content']
        else:return None
    except Exception: return None
