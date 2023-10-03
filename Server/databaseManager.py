import sqlite3


@DeprecationWarning
class Manager:

    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        if self.cursor.execute('SELECT name FROM sqlite_master').fetchone() is None:
            self.cursor.execute('CREATE TABLE patients(id INTEGER PRIMARY KEY AUTOINCREMENT, medicalId INTEGER NOT NULL, name TEXT NOT NULL)')
            self.cursor.execute('CREATE TABLE reports(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'patient_id INTEGER REFERENCES patients(id) ON UPDATE CASCADE ON DELETE SET NULL,'
                        'date DATE NOT NULL, symptoms TEXT, paramBitalino TEXT NOT NULL, HpComments TEXT)')
            
    def createPatient(self, medicalId:int, name:str):
        self.cursor.execute('INSERT INTO patients (medicalId, name) VALUES ('+medicalId+', '+name+')')

    def deletePatient(self, id:int):
        self.cursor.execute('DELETE FROM patients WHERE id = '+id)

    def modifySymptoms(self, id:int, text:str):
        self.cursor.execute('UPDATE reports SET symptoms='+text+' WHERE patient_id='+id)

    def modifyHpComments(self, id:int, text:str):
        self.cursor.execute('UPDATE reports SET HpComments='+text+' WHERE patient_id='+id)

    def modifyparamBitalino(self, id:int, text:str):
        self.cursor.execute('UPDATE reports SET paramBitalino='+text+' WHERE patient_id='+id)

    def setUp(self):
        self.cursor.execute("CREATE TABLE users("+
                       "userId INTEGER PRIMARY KEY ON DELETE CASCADE NOT NULL AUTOINCREMENT,"+
                       "username TEXT NOT NULL,"+
                       "userType TEXT NOT NULL,"+
                       "password BLOB NOT NULL)")
                    
    def checkUser(self,username:str,password:bytes):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=? LIMIT 1",(username,password))
        return self.cursor.fetchone()

    
    def createUser(self, username:str, password:bytes, userType:str):
        '''Raises ValueError if userType is not admin, patient or clinician'''
        if userType not in ("admin", "patient","clinician"): raise ValueError
        self.cursor.execute("INSERT INTO users (userId, username, userType, password) VALUES (?,?,?)",(username,password,userType))
        

    def deleteUser(self, userId:int):
        self.cursor.execute("DELETE * FROM users WHERE userId = ?",(userId,))
