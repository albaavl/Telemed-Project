import os,math,re


#Generic fn

def logIn():
    '''Ask user username and password via terminal, returns: User, Password'''
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


def patient_bitalinoError():
    os.system('cls' if os.name=='nt' else 'clear')
    print("The MAC address introduced was wrong or the device could not be found.")
    input("Press enter to back to main menu...")


def patient_mainMenu()->int:
    '''Generates the main menu for the user, returns the option chosen by the user: 1-New medical report; 2-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1.Place a new medical report.")
    print("  2.Log out.")
    while True:
        usrin=input("Please select one option: ")
        try: return int(usrin)
        except ValueError: 
            print("That's not a number. Please introduce a valid option.")


def patient_askForSymptoms()->str:
    '''Ask user via terminal for the symptoms, returns an unchecked string provided by the user'''
    os.system('cls' if os.name=='nt' else 'clear')
    return input("Please introduce your symptoms below:\n")


def patient_askForParameters()->bool:
    '''Ask user via terminal whether they want to record parameters or not, returns `True`/`False`.'''
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        i=input("Would you like to record parameters with your bitalino device? (y/n)")
        if i.capitalize() in ("Yes","Y","Si","S"): return True
        elif i.capitalize() in ("No", "N"): return False


def patient_errorWithParams(error):
    print('Something went wrong while sending data to the server. Please try again later.')
    print(error)
    input("Press enter to go back into main menu...")

#Clinician only

def clinician_mainMenu():
    '''Generates the main menu for the health expert, returns the option chosen by the user: 1-Show patients; 2-Show reports; 3-Add comment; 4-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1. Show patients.")
    print("  2. Add comment to reports.")
    print("  3. Log out.")

    while True:
        try:
            option = int(input("Please select one option: "))
            if option in [1, 2, 3]:
                return option
            else:
                print("Invalid option. Please enter a number within the valid range.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def clinician_showPatients(patients: list):
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available patients:")

    for patient in patients:
        print("PatientID: " + str(patient[0]) + " - Name: " + patient[1])

def clinician_selectOption(pat_or_rep: list):
    options = []
    for pr in pat_or_rep:
        options.append(pr[0])
    while True:
        try:
            opt = int(input("Please select one option: "))
            if opt in options:
                return opt
            else:
                print("Invalid option. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def clinician_showReports(reports: list):
    '''Shows the reports of the patient in the terminal'''
    os.system('cls' if os.name=='nt' else 'clear')
    if not reports:
        print("No reports available.")
    else:
        print("Available reports:")
        for report in reports:
            print("ReportID " + str(report[0]) + " - " + report[2])

   

def clinician_showSelectedReport(reports: list, report_ID):
    '''Shows the data of the selected report in the terminal'''
    os.system('cls' if os.name =='nt' else 'clear')
    for report in reports:
        if report[0] == report_ID:
            break
    if not report:
        print("No report.")
        return input("Press enter to continue...")
    else:
        print("Report data:")
        print("Report ID: " + str(report[0]))
        print("Date: " + str(report[2]))
        print("Symptoms: " + report[3])
        if report[4]!= None:
            print("Bitalino signal: " + report[4])
        else:
            print("No Bitalino signal recorded")
        print("Comments: " + report[5])

def clinician_addComment():
    '''Ask user via terminal for the comment, returns an unchecked string provided by the user'''
    os.system('cls' if os.name=='nt' else 'clear')
    comment = input("Please introduce your comment below:\n")
    return comment

def clinician_errorRetrievingInfoFromServer():
    print('Something went wrong while getting the information from the server. Please try again later.')
    input("Press enter to go back into main menu...")

def clinician_failedCommentCreation():
    print('Something went wrong while sending data to the server. Please try again later.')
    input("Press enter to go back into main menu...")



#Admin only

def admin_mainMenu()->int:
    '''Generates the main menu for the user, returns the option chosen by the user: 1-Add user; 2-Delete user; 3-Logout'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("Available options:")
    print("  1.Create a new user.")
    print("  2.Delete selected user.")
    print("  3.Shut down server.")
    print("  4.Log out.")
    while True:
        usrin=input("Please select one option: ")
        try: return int(usrin)
        except ValueError: 
            print("That's not a number. Please introduce a valid option.")

def admin_addUser():
    '''Prompts user for data necesary to create a new user into the system.\n
        Returns the user data required to create a new user, or None if user
        wants to go back without creating a new user.'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("--- Create new user ---")
    print("Leave name field empty to go back into main menu.")
    name=input("User name:")
    if name == "": return (None,None,None)
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


def admin_selectUserForDeletion(lst:list)->(int,None):
    '''Provided an user list, will print display all of the users, and ask the user for
        an user ID (user to be deleted), if the userID provided is within the range of
        user ids of the list, it will be returned (`int`). Otherwise return `None`.'''
    os.system('cls' if os.name=='nt' else 'clear')
    print("--- Users registered in the system ---\n")
    print("ID     Role          Name")
    for p in lst:
        for s in (0,2,1):
            if s==0:
                print(p[s],end="")
                i=math.floor(math.log10(p[s]))
                if 7-i >= 0: 
                    for j in range(6-i):print(" ", end="")
            elif s==2:
                print(p[s].capitalize(),end="")
                if 14-p[s].__len__() >= 0:
                    for j in range(14-p[s].__len__()):print(" ", end="")

        print("")

    while True:
        usrin=input("\nPlease select one user ID (Introduce any value to go back to main menu): ")
        try: 
            deleteID = int(usrin)
            for p in lst:
                if deleteID == p[0]: return deleteID
            return None
        except ValueError: 
            print("That's not a number. Please introduce a valid option.")
            print("If you want to go back to the main menu, introduce a number that doesnt correspond to any userID.")

            
def printErrors(error):
    try:
        print(error[0])
    except:
        print(error)
