import hashlib
import sqlite3

class Manager:

    def __init__(self):
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
                                'date DATE NOT NULL, symptoms TEXT, paramBitalino TEXT NOT NULL, HpComments TEXT)')
            self.createUser('admin',self.generatePswHash('admin'), 'admin')
            self.createUser('patient', self.generatePswHash('patient'), 'patient')
            self.createUser('clinician', self.generatePswHash('clinician'), 'clinician')


    #devuelve el userType en caso de existir el usuario y contraseña y si no existe devuelve excepcion
    def checkUser(self,username:str,password =b'admin'):
        self.cursor.execute("SELECT userType FROM users WHERE username=? AND password=?", (username, password))
        user_type = self.cursor.fetchone()
        #tiene que devolver solo el tipo de usuario que es y si no esta en la tabla lanzar una excepcion
        if user_type:
            return user_type[0]
        else:
            raise ValueError(f"user not found")
        


    def createUser(self, username:str, password:bytes, userType:str):
        '''Raises ValueError if userType is not admin, patient or clinician'''
        if userType not in ("admin", "patient","clinician"): raise ValueError(f"Invalid usertype, you have to choose between admin, patient or clinician") #añadiria texto al pq del value error para poder mandarlo al cliente y que se entienda cual es el error
        #username deberia ser unico aka comprobar que no hay otro y sino tbb error
        self.cursor.execute("SELECT username FROM users WHERE username = ?",(username,))
        existing_username = self.cursor.fetchone()
        if existing_username:
            raise ValueError(f"Username already taken, please choose a different username")
        self.cursor.execute("INSERT INTO users (userId, username, userType, password) VALUES (?,?,?)",(username,password,userType))
        self.connection.commit()
        return True
        #devolver algo si se ha añadido bien, maybe un true?

    def deleteUser(self, userId:int):
        self.cursor.execute("DELETE * FROM users WHERE userId = ?",(userId,))
        #lo mismo que en createUser, devolveria algo para hacer el check de que t o d o guay
        #no hay forma de checkear que ha ido bien porque lo unico que linkea es userId y una vez
        #que se borra hace cascada y es reutilizada por otro user
        return True #pongo esto para que Alba esté contenta :))        

    def new_report(self, patient_id, date, symptoms, paramBitalino, HpComments):
        self.cursor.execute("INSERT INTO reports (patient_id, date, symptoms, paramBitalino, HpComments) VALUES (?, ?, ?, ?, ?)",
                            (patient_id,date,symptoms, paramBitalino, HpComments))
        self.connection.commit()

    def get_patients(self):
        #que devuelva una lista con todos los pacientes (userdID, username), error si no hay con explicacion
        try:
            self.cursor.execute("SELECT userId, username FROM users WHERE userType = 'patient'")
            patients = self.cursor.fetchall()
            return patients
        except Exception as e:
            raise ValueError(f"Failed to retrieve the list of patients")

    def get_reports(self, patientId):
        #que devuelva una lista con todos los reports del paciente (todos los parametros), error si no hay con explicacion
        try:
            self.cursor.execute("SELECT * FROM reports WHERE patient_id = ?", (patientId,))
            reports = self.cursor.fetchall()
            return reports
        except Exception as e:
            raise ValueError(f"Failed to retrieve the list of reports")

    def add_comments(self, reportId, comments):
        try:
            self.cursor.execute("UPDATE reports SET HpComments = ? WHERE id = ?", (comments, reportId))
            return True
        except Exception as e:
            raise ValueError(f"Failed to update comments")

    def generatePswHash(self,password:str):
        hashgen = hashlib.sha512()
        hashgen.update(password.encode('utf8'))
        return hashgen.digest()