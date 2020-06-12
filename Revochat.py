from firebase import firebase
import sys

# <----Universal Functions---->
def getCommand():
    command = input("Are you a New User(n) or Existing User(e): ")
    if command == "n":
        Register()
    elif command == "e":
        login()

def Welcome():
    print("<<--------------------------  Welcome to RevoChat, A Terminal Chat App -------------------------->>" + "\n")

def writeData(entry, tag, location):
    contents = []
    contents.append(entry)
    database.post('/Chat/{}'.format(tag), contents)

def readData(tag):
    data = database.get('Chat/{}'.format(tag), None)
    return data

def CheckCreds(name, username, password):
    if len(username) or len(password) == 0:
        print("**Enter a valid username and password, one that is not left blank/empty**" + "\n")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()

    if username.find("@") or username.find(".com") == -1:
        print("The username must be an email" + "\n")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()
    
    elif len(password) < 6:
        print("Your password is too weak! (length < 6 characters)")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")

    else:
        print("**Account successfully created**")
        print("You will be redirected to the login screen")
        writeData(name, "names", 2)
        writeData(username, "Usernames", 0)
        writeData(password, "Passwords", 1)
        login()


# <----Universal Functions---->

def Register():
    Welcome()
    print("<<-------------------- Register Account ---------------------->>")
    print("As this is just a simple app for testing purposes, do not use actual credentials for registration" + "\n")
    name = str(input("Your Name: "))
    username = str(input("Set your username: "))
    password = input("Set a password: ")
    CheckCreds(name, username, password)

def login():
    Welcome()
    print("<<-------------------- Login Screen ---------------------->>")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    usernames = readData("Usernames")
    passwords = readData("Passwords")
    if username in usernames and password in passwords:
        print("**You have successfully logged into your account!**")
        print("You can now begin sending messages to your friends!")
        LoadMessages()
        SendMessages()
    else:
        print("Your login credentials do not match the registered credentials")
        login()

def SendMessages():
    print("<<-------------------- Revo Messages ---------------------->>")
    sender = str(input("Your Name: "))
    recipient = input("Name of the Recipient: ")
    while True:
        message = input("Enter a message: ")
        if sender and recipient in readData("names"):
            context = "{} --> {}".format(sender, recipient )
            message = context + "\n" + message
            writeData(message, "messages", 4)
            command = input("Load Messages?(y/N) or exit(e): ")
            if command == "y":
                LoadMessages()
            elif command == "N":
                SendMessages()
            elif command == "e":
                print("**Thanks for using Revochat, hope to see you later!**") 
                sys.exit()

def LoadMessages():
    print("<<--------------------------- Your Messages --------------------------->>")
    messages = readData("messages")
    for message in messages:
        print(message)
        print("---------------------------------------------------------------------------")


database = firebase.FirebaseApplication("https://revochat-78efd.firebaseio.com/", None)
getCommand()