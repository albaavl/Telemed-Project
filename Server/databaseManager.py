import sqlite3


class Manager:

    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        if self.cursor.execute('SELECT name FROM sqlite_master').fetchone() is None:
            self.cursor.execute('CREATE TABLE patients(id INTEGER PRIMARY KEY AUTOINCREMENT, medicalId INTEGER NOT NULL, name TEXT NOT NULL)')
            self.cursor.execute('CREATE TABLE reports(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'patient_id INTEGER REFERENCES patients(id) ON UPDATE CASCADE ON DELETE SET NULL,'
                        'date DATE NOT NULL, symptoms TEXT, paramBitalino TEXT NOT NULL, HpComments TEXT)')
            
    def createPatient(self, medicalId, name):
        self.cursor.execute('INSERT INTO patients (medicalId, name) VALUES ('+medicalId+', '+name+')')

    def deletePatient(self, id):
        self.cursor.execute('DELETE FROM patients WHERE id = '+id)

    def modifySymptoms(self, id, text):
        self.cursor.execute('UPDATE reports SET symptoms='+text+' WHERE patient_id='+id)

    def modifyHpComments(self, id, text):
        self.cursor.execute('UPDATE reports SET HpComments='+text+' WHERE patient_id='+id)

    def modifyparamBitalino(self, id, text):
        self.cursor.execute('UPDATE reports SET paramBitalino='+text+' WHERE patient_id='+id)
