import sqlite3

def __init():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if cursor.execute('SELECT name FROM sqlite_master').fetchone() is None:
        cursor.execute('CREATE TABLE patients(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)')
        cursor.execute('CREATE TABLE reports(id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER REFERENCES patients(id) ON UPDATE CASCADE ON DELETE SET NULL, date DATE NOT NULL, symptoms TEXT, paramBitalino TEXT NOT NULL, HpComments TEXT)')

