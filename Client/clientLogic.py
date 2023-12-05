import hashlib, json, pickle
import time
from json import JSONDecodeError

from bitalino import BITalino as bit

#   Module that contains all client functions that have functionallity. 
#   No user inputs will be taken by this functions, nor they will output any value to std out

def generatePswHash(password:str) -> bytes:
    '''For a given password `string`, its encrypted and returned as `bytes`'''
    hashgen = hashlib.sha512()
    hashgen.update(password.encode('utf8'))
    return hashgen.digest()

def sendLoginCredentials(usr:str,psw:bytes) -> bytes:
    '''Requires username `string` and password `bytes`, returns log in
        query in bytes'''
    return pickle.dumps({'control':'login','content':[usr,psw]}) 

def decodeServerResponse(query:bytes) -> bytes:
    '''Return `content` AKA the response value, or  `None` if the response has invalid format.\n
        If the response was an error type, the error msg will be returned inside a `tuple`.'''
    try:
        response=json.loads(query)
        if not response: return None
        if response['control'] == 'success': return response['content']
        elif response['control'] == 'error': return (response['content'],)
        else:return None
    except JSONDecodeError: 
        raise ValueError('Invalid format for server response')



#Patient Only    

def patient_connectToBitalino(mac:str, running_time = 60) -> (list):
    try:
        acqChannels = [2]
        samplingRate = 100
        nSamples = 10
        digitalOutput_on = [1, 1]
        digitalOutput_off = [0, 0]
        # Connect to BITalino
        device = bit(mac)
        device.start(samplingRate, acqChannels)
        start = time.time()
        end = time.time()
        data = ''
        device.trigger(digitalOutput_on)
        while (end - start) < running_time:
            # Read samples
            data += str(device.read(nSamples))
            end = time.time()
        # Turn BITalino led and buzzer off
        device.trigger(digitalOutput_off)
        # Stop acquisition
        device.stop()
        # Close connection
        device.close()
        return data
    except Exception as e:
        print(e)
        return None


def patient_sendReport(patientInput:tuple, clientId:int, params:list=None):
    '''Sends report data to server'''
    inputData=[clientId,patientInput[0],patientInput[1],patientInput[2],patientInput[3]]
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

def admin_createUser(name:str, psw:bytes, userType:str) -> bytes:
    '''Generate query to create a new User: \n >`name` must be provided as an `string`.
        \n >`password` must be bytes, preferrably encrypted (Bytes will be sent as provided). \nReturns the query in `bytes`.'''
    userData=(name,psw,userType)    
    return pickle.dumps({'control':'add_user','content':userData})

def admin_showAllUsers() -> bytes:
    '''Generates query to get all users from database. No input required. Returns the query in `bytes`.'''
    return json.dumps({'control':'show_users'}).encode('utf8')

def admin_deleteUser(userID:int) -> bytes:
    '''Generates user deletion query, requires the userID of the target user.Returns the query in `bytes`.'''
    return json.dumps({'control':'delete_user','content':userID}).encode('utf8')

def admin_shutdown() -> bytes:
    '''Generate shutdown query, returns `Bytes`. No input required'''
    return json.dumps({'control':'shut_down','content':"Shut down, now. (つ｡◕‿‿◕｡)つ Plz"}).encode('utf8')