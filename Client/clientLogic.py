import hashlib


def generatePswHash(password:str):
    hashgen = hashlib.sha512()
    hashgen.update(password.encode('utf8'))
    return hashgen.digest()

def connectToBitalino(mac:str):
    pass


def generateParamsQuery(symptoms:str, params:str=None):
    if params != None: return symptoms.encode('utf8')+b' '+params.encode('utf8') #TODO Any dict?
    return symptoms.encode('utf8')

