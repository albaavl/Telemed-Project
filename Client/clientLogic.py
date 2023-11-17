import hashlib, json, pickle, os
import time

from bitalino import BITalino as bit


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

def patient_connectToBitalino(mac:str="20:16:07:18:17:85", running_time = 5) -> (list):
    acqChannels = [2]
    samplingRate = 1000
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