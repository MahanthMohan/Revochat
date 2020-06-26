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

def writeData(entry, tag):
    contents = []
    contents.append(entry)
    database.post('/Chat/{}'.format(tag), contents)

def readData(tag):
    data = database.get('/Chat/{}'.format(tag), None)
    return data

def LoadMessages():
    print("<<--------------------------- Your Messages --------------------------->>")
    messages = str(readData('Messages'))
    messagelist = messages.split(",")
    for message in messagelist:
        print(message)
        print("---------------------------------------------------------------------------")

def getCreds():
    username_list = list(readData('Usernames').items())
    password_list = list(readData('Passwords').items())
    usernames = []
    passwords = []
    for i in range (0, len(username_list)):
        username_list[i] = list(username_list[i])
        username_list[i] = username_list[i][1]
        usernames.append(username_list[i][0])

    for n in range (0, len(password_list)):
        password_list[n] = list(password_list[n])
        password_list[n] = password_list[n][1]
        passwords.append(password_list[n][0])
        
    return [usernames, passwords]

# <----Universal Functions---->

def Register():
    Welcome()
    print("<<-------------------- Register Account ---------------------->>")
    print("As this is just a simple app for testing purposes, do not use actual credentials for registration" + "\n")
    name = str(input("Your Name: "))
    username = input("Set your username: ")
    password = input("Set a password: ")
    usernames = str(readData('Usernames'))
    passwords = str(readData('Passwords'))

    if len(username) == 0 and len(password) == 0:
        print("**Enter a valid username and password, one that is not left blank/empty**" + "\n")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()

    if username.find("@") == -1 or username.find(".com") == -1:
        print("**The username must be an email**" + "\n")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()

    if username in getCreds()[0] or password in getCreds()[1]:
        print("**Account already registered**")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()
    
    if len(password) < 6:
        print("**Your password is too weak**")
        print("--------------->> You will be redirected to Register Account --------->>" + "\n")
        Register()

    else:
        print("**Account successfully created**")
        print("You will be redirected to the login screen")
        writeData(name, "Names")
        writeData(username, "Usernames")
        writeData(password, "Passwords")
        login()

def login():
    Welcome()
    print("<<-------------------- Login Screen ---------------------->>")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    usernames = getCreds()[0]
    passwords = getCreds()[1]

    for i in range (0, len(usernames)):
        for n in range (0, len(passwords)):
            if usernames[i] == username and passwords[n] == password:
                print("**You have successfully logged into your account!**")
                print("You can now begin sending messages to your friends!")
                LoadMessages()
                SendMessages(10) # You can add a max messages parameter to the function (Default -> 10)
            else:
                print("Your login credentials do not match the registered credentials")
                sys.exit()


def SendMessages(max):
    sender = str(input("Your Name: "))
    reciever = str(input("Name of the Reciever: "))
    names = str(readData('Names'))
    context = "({} --> {}) ".format(sender, reciever)
    for i in range(0, max):
        if names.find(sender) and names.find(reciever):
            message = input("Message: ")
            message = context + message
            writeData(message, "Messages")
            command = input("Load Messages?(y/N) or exit(e): ")
            if command == "y":
                LoadMessages()
            elif command == "N":
                SendMessages()
            elif command == "e":
                print("**Thanks for using Revochat, hope to see you later!**") 
                sys.exit()
 

database = firebase.FirebaseApplication("https://revochat-78efd.firebaseio.com/", None)
getCommand()
