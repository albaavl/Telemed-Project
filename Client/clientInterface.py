import os
import re


#Generic fn

def logIn():
    '''Ask user username and password via terminal, returns (User, Password)'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("-- Welcome to our client App --")
    username = input("Please introduce your username: ")
    password = input("Please introduce your password: ")
    return username,password


def wrongLogIn(error):
    '''Wrong username/password combination'''
    os.system('cls' if os.name=='nt' else 'clear')
    for e in error:
        print(e)
    # print("Wrong username or password, please try again.")
    input("Press enter to continue...")

def success():
    print("Data sent successfully.")
    input("Press intro to go back into the main menu.")

def wrongOption():
    os.system('cls' if os.name=='nt' else 'clear')
    print("The chosen option is not valid.")
    input("Press enter to continue...")

#Patient only    

def patient_askForBitalinoMAC():
    '''Propmt for Bitalino MAC address in console, input is not checked.'''
    os.system('cls' if os.name=='nt' else 'clear')
    return input("Please introduce the MAC address of your bitalino device: ")


def patient_wrongMAC():
    os.system('cls' if os.name=='nt' else 'clear')
    print("The MAC address introduced was wrong or the device could not be found.")


def patient_mainMenu():
    '''Generates the main menu for the user, returns the option chosen by the user: 1-New medical report; 2-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1.Place a new medical report.")
    print("  2.Log out.")
    return int(input("Please select one option: "))


def patient_askForSymptoms():
    '''Ask user via terminal for the symptoms, returns an unchecked string provided by the user'''
    os.system('cls' if os.name=='nt' else 'clear')
    return input("Please introduce your symptoms below:\n")


def patient_askForParameters():
    '''Ask user via terminal whether they want to record parameters or not, returns True/False'''
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        i=input("Would you like to record parameters with your bitalino device? (y/n)")
        if i.capitalize() in ("YES","Y","SI","S"): return True
        elif i.capitalize() in ("NO", "N"): return False


def patient_errorWithParams(error):
    print('Something went wrong while sending data to the server. Please try again later.')
    print(error)
    input("Press enter to go back into main menu...")

#Clinician only

def clinician_mainMenu():
    '''Generates the main menu for the health expert, returns the option chosen by the user: 1-Show patients; 2-Show reports; 3-Add comment; 4-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1.Show patients.")
    print("  2.Add comment to reports.")
    print("  3.Log out.")
    return int(input("Please select one option: "))

def clinician_showPatients(patients: list):
    '''Shows the list of patients in the terminal, returns the selected patient'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available patients:")
    for i in range(len(patients)):
        print("Patient " + str(patients[i][0]) + " - " + patients[i][1])
    opt=int(input("Please select one option: "))
    return opt

def clinician_showPatientReports(reports: list):
    '''Shows the data of the patient in the terminal, returns the selected report'''
    os.system('cls' if os.name=='nt' else 'clear')
    if not reports:
        print("No reports available.")
        return reports
    else:
        print("Available reports:")
        for i in range(len(reports)):
            print("Report " + str(i+1) + " - " + reports[i][2])
        while True:
            try:
                opt = int(input("Please select one report (enter the corresponding number): "))
                if 1 <= opt <= len(reports):
                    break
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.") 

    return reports[opt - 1]
   

def clinician_showSelectedReport(report: list):
    print()
    '''Shows the data of the selected report in the terminal'''
    os.system('cls' if os.name=='nt' else 'clear')
    if not report:
        print("No report available.")
        return input("Press enter to continue...")
    else:
        for i in range(len(report)):
            if not report[i]:
                report[i] = "No data available."

        print("Report data:\n")
        print("Date:\n" + str(report[2]) +"\n")
        print("Symptoms:\n" + report[3] +"\n")
        print("Bitalino signal\n:" + report[4] +"\n")
        print("Comments:\n" + report[5] +"\n")
    return input("Press enter to continue...")
 

def clinician_errorWithPatients():
    print('Something went wrong while getting the information from the server. Please try again later.')
    input("Press enter to go back into main menu...")

def clinician_addComment(previous_comment: str):
    '''Ask user via terminal for the comment, returns an unchecked string provided by the user'''
    os.system('cls' if os.name=='nt' else 'clear')
    comment = input("Please introduce your comment below:\n")
    pattern = "No data available."
    new_comment = re.sub(pattern, '', previous_comment)
    complete_comment = new_comment + "\n" + comment
    return complete_comment

def clinician_failedCommentCreation():
    print('Something went wrong while sending data to the server. Please try again later.')

#Admin only

def admin_mainMenu():
    '''Generates the main menu for the user, returns the option chosen by the user: 1-Add user; 2-Delete user; 3-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1.Create a new user.")
    print("  2.Delete selected user.")
    print("  3.Log out.")
    return int(input("Please select one option: "))

def admin_addUser():
    os.system('cls' if os.name=='nt' else 'clear')
    print("--- Create new user ---")
    print("Leave name field empty to go back into main menu.")
    name=input("User name:")
    if name == "\n": return None
    psw=input("User password:")
    while True:
        t=input("User type (Admin/Clinician/Patient): ")
        t=t.capitalize()
        if t in ("Admin", "A"): return (name, psw, "admin")
        elif t in ( "Clinician", "C"): return (name, psw, "clinician")
        elif t in ("Patient", "P"): return (name, psw, "patient")
        else: 
            print("Invalid user type, please use Admin/A, Clinician/C or Patient/P")
            input("Press intro to continue...")

def admin_failedUserCreation(error):
    print(error)
    input("shiet")

def admin_selectUser(lst:list):
    print(lst)
    return input("Please introduce an user id to delete: ")