import os


    
def startUp():
    os.system("cls")
    print("-- Welcome to our client App --")
    u = input("Please introduce your username: ")
    p = input("Please introduce your password: ")
    return u,p

def wrongLogIn():
    os.system("cls")
    print("Wrong user or password, please try again.")
    input("Press enter to continue...")
    

def askForBitalinoMAC():
    os.system("cls")
    return input("Please introduce the MAC address of your bitalino device: ")

def wrongMAC():
    os.system("cls")
    print("The MAC address introduced was wrong or the device could not be found.")

def mainMenu():
    os.system("cls")
    print("Available options:")
    print("  1.Place a new medical report.")
    print("  2.Log out.")
    return int(input("Please select one option: "))

def wrongOption():
    os.system("cls")
    print("The chosen option is not valid.")
    input("Press enter to continue...")

def askForSymptoms():
    os.system("cls")
    return input("Please introduce your symptoms below:\n")

def askForParameters():
    while True:
        os.system("cls")
        i=input("Would you like to record parameters with your bitalino device? (y/n)")
        if i.capitalize in ("YES","Y","SI","S"): return True
        elif i.capitalize in ("NO", "N"): return False

def success():
    print("Data sent successfully.")
    input("Press intro to go back into the main menu.")