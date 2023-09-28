import hashlib, pickle


def generatePswHash(password:str):
    hashgen = hashlib.sha512()
    hashgen.update(password.encode('utf8'))
    return hashgen.digest()

def connectToBitalino(mac:str):
    pass


def generateParamsQuery(patientInput:str, params:str=None):
    '''`Content With params->` <symptoms:>patientInput<data:>params
    
    `Content With no params->` patientInput'''
    if params != None: return pickle.dumps({'control':'new_report','content':"<symptoms:>"+patientInput+"<data:>"+params}) 
    #TODO @alba your choice on query struct
    return pickle.dumps({'control':'new_report','content':patientInput})

def generateLogInQuery(usr:str,psw:bytes):
    return pickle.dumps({'control':'login','content':'query'})#TODO CHANGE QUERY FOR THE ACTUAL LOGIN QUERY


def decodeQuery(query:bytes)->(str|None):
    '''Return `(str)content` AKA the response value, or  `None` if the response has invalid format'''
    try:
        response=pickle.loads(query)
        if not response: return None
        if response['control'] in ('success','error'): return response['content']
        else:return None
    except Exception: return None
