import os

#Generic fn

def logIn():
    '''Ask user username and password via terminal, returns (User, Password)'''
    os.system("cls")
    print("-- Welcome to our client App --")
    username = input("Please introduce your username: ")
    password = input("Please introduce your password: ")
    return username,password


def wrongLogIn():
    '''Wrong username/password combination'''
    os.system("cls")
    print("Wrong username or password, please try again.")
    input("Press enter to continue...")

def success():
    print("Data sent successfully.")
    input("Press intro to go back into the main menu.")

def wrongOption():
    os.system("cls")
    print("The chosen option is not valid.")
    input("Press enter to continue...")

#Patient only    

def patient_askForBitalinoMAC():
    '''Propmt for Bitalino MAC address in console, input is not checked.'''
    os.system("cls")
    return input("Please introduce the MAC address of your bitalino device: ")


def patient_wrongMAC():
    os.system("cls")
    print("The MAC address introduced was wrong or the device could not be found.")


def patient_mainMenu():
    '''Generates the main menu for the user, returns the option chosen by the user: 1-New medical report; 2-Logout'''
    os.system("cls")
    print("Available options:")
    print("  1.Place a new medical report.")
    print("  2.Log out.")
    return int(input("Please select one option: "))


def patient_askForSymptoms():
    '''Ask user via terminal for the symptoms, returns an unchecked string provided by the user'''
    os.system("cls")
    return input("Please introduce your symptoms below:\n")


def patient_askForParameters():
    '''Ask user via terminal whether they want to record parameters or not, returns True/False'''
    while True:
        os.system("cls")
        i=input("Would you like to record parameters with your bitalino device? (y/n)")
        if i.capitalize in ("YES","Y","SI","S"): return True
        elif i.capitalize in ("NO", "N"): return False


def patient_errorWithParams():
    print('Something went wrong while sending data to the server. Please try again later.')
    input("Press enter to go back into main menu...")

#Clinician only

def clinician_mainMenu():
    '''Generates the main menu for the health expert, returns the option chosen by the user: 1-Show patients; 2-Show reports; 3-Add comment; 4-Logout'''
    os.system("cls")
    print("Available options:")
    print("  1.Show patients.")
    print("  2.Show reports.")
    print("  3.Add comment to a report.")
    print("  4.Log out.")
    return int(input("Please select one option: "))

def clinician_showPatients(patients: list):
    '''Shows the list of patients in the terminal, returns the selected patient'''
    os.system("cls")
    print("Available patients:")
    for i in range(len(patients)):
        print("  "+str(i+1)+". "+patients[i])
    opt=int(input("Please select one option: "))
    return opt-1

def clinician_showPatientReports(reports: list):
    '''Shows the data of the patient in the terminal, returns the selected report'''
    os.system("cls")
    print("Available reports:")
    for i in range(len(reports)):
        print("  "+str(i+1)+". "+reports[i])
    opt=int(input("Please select one option: "))
    return reports[opt-1]

def showSelectedReport(report: list):
    '''Shows the data of the selected report in the terminal'''
    #No tengo muy claro como esta estructurado el contenido del reporte, asi que lo dejo como lista por si acaso
    print("Report data:")
    print("  Date: "+report[0])
    print("  Symptoms: "+report[1])
    print("  Signal: "+report[2])
    print("  Comments: "+report[3])

def clinician_errorWithPatients():
    print('Something went wrong while getting the information from the server. Please try again later.')
    input("Press enter to go back into main menu...")

def clinitian_addComment():
    '''Ask user via terminal for the comment, returns an unchecked string provided by the user'''
    os.system("cls")
    return input("Please introduce your comment below:\n")

#Admin only

def admin_mainMenu():
    '''Generates the main menu for the user, returns the option chosen by the user: 1-Add user; 2-Delete user; 3-Logout'''
    os.system("cls")
    print("Available options:")
    print("  1.Create a new user.")
    print("  2.Delete selected user.")
    print("  3.Log out.")
    return int(input("Please select one option: "))

def admin_addUser():
    os.system("cls")
    print("--- Create new user ---")
    print("Leave name field empty to go back into main menu.")
    name=input("User name:")
    if name == "\n": return None
    psw=input("User password:")
    while True:
        t=input("User type (Admin/Clinician/Patient): ")
        t=t.capitalize()
        if t in ("ADMIN", "A"): return (name, psw, "admin")
        elif t in ( "CLINICIAN", "C"): return (name, psw, "clinician")
        elif t in ("PATIENT", "P"): return (name, psw, "patient")
        else: 
            print("Invalid user type, please use Admin/A, Clinician/C or Patient/P")
            input("Press intro to continue...")

def admin_failedUserCreation():
    pass

def admin_selectUser():
    pass