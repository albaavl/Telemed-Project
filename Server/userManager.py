import sqlite3

@DeprecationWarning
class userManager:

    connection = sqlite3.connect('database.db')
    cursor=connection.cursor()

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

    #TODO merge with the normal sql manager.
