import base64
import hashlib
import sqlite3

class Manager:

    def __init__(self):
        '''connects to db and creates the users and reports tables'''
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        if self.cursor.execute('SELECT name FROM sqlite_master').fetchone() is None:
            self.cursor.execute("CREATE TABLE users(" +
                                "userId INTEGER PRIMARY KEY NOT NULL," +
                                "username TEXT NOT NULL," +
                                "password BLOB NOT NULL," +
                                "userType TEXT NOT NULL)")

            self.cursor.execute('CREATE TABLE reports(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                'patient_id INTEGER REFERENCES users(userId) ON UPDATE CASCADE ON DELETE SET NULL,'
                                'date DATE NOT NULL, fatigue BOOLEAN, dizziness BOOLEAN, sweating BOOLEAN, symptoms TEXT, paramBitalino TEXT, HpComments TEXT)')
            self.createUser('admin',self.generatePswHash('admin'), 'admin')
            self.createUser('patient', self.generatePswHash('patient'), 'patient')
            self.createUser('clinician', self.generatePswHash('clinician'), 'clinician')


    def checkUser(self,username:str,password =b'admin'):
        '''returns the user and password if they exist and if not it gives an exception'''
        self.cursor.execute("SELECT userType,userId FROM users WHERE username=? AND password=?", (username, password))
        user_type = self.cursor.fetchone()
        if user_type:
            return user_type
        else:
            raise ValueError(f"user not found")
        


    def createUser(self, username:str, password:bytes, userType:str):
        '''creates the user with the password and user provided and Raises ValueError if userType is not admin, patient or clinician'''
        if userType not in ("admin", "patient","clinician"): raise ValueError(f"Invalid usertype, you have to choose between admin, patient or clinician") #añadiria texto al pq del value error para poder mandarlo al cliente y que se entienda cual es el error
        #username deberia ser unico aka comprobar que no hay otro y sino tbb error
        self.cursor.execute("SELECT username FROM users WHERE username = ?",(username,))
        existing_username = self.cursor.fetchone()
        if existing_username:
            raise ValueError(f"Username already taken, please choose a different username")
        self.cursor.execute("INSERT INTO users (username, password, userType) VALUES (?,?,?)",(username,password,userType))
        self.connection.commit()
        return True
        #devolver algo si se ha añadido bien, maybe un true?

    def deleteUser(self, userId:int):
        '''deletes the user provided via id'''
        self.cursor.execute("DELETE FROM users WHERE userId = ?",(userId,))
        return True #pongo esto para que Alba esté contenta :))        

    def new_report(self, patient_id, fatigue, dizziness, sweating, symptoms, paramBitalino, date, HpComments= None):
        '''adds report to the reports table'''
        self.cursor.execute("INSERT INTO reports (patient_id, date,fatigue, dizziness, sweating, symptoms, paramBitalino, HpComments) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (patient_id, date,fatigue, dizziness, sweating, symptoms, paramBitalino, HpComments))
        self.connection.commit()

    def get_patients(self):
        '''returns a list with all the patients (userID and username)'''
        try:
            self.cursor.execute("SELECT userId, username FROM users WHERE userType = 'patient'")
            patients = self.cursor.fetchall()
            return patients
        except Exception as e:
            raise ValueError(f"Failed to retrieve the list of patients")
    
    def get_users(self):
        '''returns a list with all users (userID, username and usertype)'''
        try:
            self.cursor.execute("SELECT userId, username, userType FROM users")
            users = self.cursor.fetchall()
            return users
        except Exception as e:
            raise ValueError(f"Failed to retrieve the list of users")

    def get_reports(self, patientId):
        '''returns a list with all the reports of the specified patient'''
        try:
            self.cursor.execute("SELECT id, date FROM reports WHERE patient_id = ?", (patientId,))
            reports = self.cursor.fetchall()
            return reports
        except Exception as e:
            raise ValueError(f"Failed to retrieve the list of reports")

    def get_selectedReport(self, reportId):
        '''returns selected report'''
        try:
            self.cursor.execute("SELECT * FROM reports WHERE id = ?", (reportId,))
            report = self.cursor.fetchone()
            return report
        except Exception as e:
            raise ValueError(f"Failed to retrieve the selected report")

    def add_comments(self, reportId, comments):
        '''adds health professional comments'''
        try:
            self.cursor.execute("UPDATE reports SET HpComments = ? WHERE id = ?", (comments, reportId))
            return True
        except Exception as e:
            raise ValueError(f"Failed to update comments")

    def generatePswHash(self, password: str) -> str:
        '''For a given password `string`, its encrypted and returned as `bytes`'''
        hashgen = hashlib.sha512()
        hashgen.update(password.encode('utf8'))
        pass_bytes = hashgen.digest()
        base64str_pass = base64.b64encode(pass_bytes).decode('utf-8')
        return base64str_pass