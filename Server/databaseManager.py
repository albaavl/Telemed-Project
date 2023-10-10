import sqlite3

class Manager:

    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        if self.cursor.execute('SELECT name FROM sqlite_master').fetchone() is None:
            self.cursor.execute("CREATE TABLE users(" +
                                "userId INTEGER PRIMARY KEY ON DELETE CASCADE NOT NULL AUTOINCREMENT," +
                                "username TEXT NOT NULL," +
                                "password BLOB NOT NULL)" +
                                "userType TEXT NOT NULL,")

            self.cursor.execute('CREATE TABLE reports(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                'patient_id INTEGER REFERENCES users(userId) ON UPDATE CASCADE ON DELETE SET NULL,'
                                'date DATE NOT NULL, symptoms TEXT, paramBitalino TEXT NOT NULL, HpComments TEXT)')



    def checkUser(self,username:str,password:bytes):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=? LIMIT 1",(username,password))
        #tiene que devolver solo el tipo de usuario que es y si no esta en la tabla lanzar una excepcion
        return self.cursor.fetchone() #not this


    def createUser(self, username:str, password:bytes, userType:str):
        '''Raises ValueError if userType is not admin, patient or clinician'''
        if userType not in ("admin", "patient","clinician"): raise ValueError #añadiria texto al pq del value error para poder mandarlo al cliente y que se entienda cual es el error
        #username deberia ser unico aka comprobar que no hay otro y sino tbb error
        self.cursor.execute("INSERT INTO users (userId, username, userType, password) VALUES (?,?,?)",(username,password,userType))
        #devolver algo si se ha añadido bien, maybe un true?

    def deleteUser(self, userId:int):
        self.cursor.execute("DELETE * FROM users WHERE userId = ?",(userId,))
        #lo mismo que en createUser, devolveria algo para hacer el check de que t o d o guay
    def new_report(self):
        #TODO create query

    def get_patients(self):
        #que devuelva una lista con todos los pacientes (userdID, username), error si no hay con explicacion

    def get_reports(self, patientId):
        #que devuelva una lista con todos los reports del paciente (todos los parametros), error si no hay con explicacion

    def add_comments(self, reportId, comments):
        #meter comments en el report y devolver algo como que ha ido bien, deberia dar error si el report no existe

