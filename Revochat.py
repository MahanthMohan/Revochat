from firebase import firebase
import json
import time
import sys

class Revochat:

# <----Universal Functions---->
    def getCommand(self):
        command = input("Are you a New User(n) or Existing User(e): " + "\n")
        if command == "n":
            Revochat.Register()
        elif command == "e":
            Revochat.login()

    def Welcome(self):
        print("<<--------------------------  Welcome to RevoChat, A Terminal Chat App -------------------------->>" + "\n")
        time.sleep(2)

    def writeData(self, data, tag, location):
        self.data = data
        self.tag = tag
        self.location = location
        with open("chat.json") as file:
            data = json.load(file)['chat'][location]
            contents = data['contents']
            contents.append(data)
        database.post('/Chat/{}'.format(tag), contents)

    def readData(self, tag):
        self.tag = tag
        data = database.get('Chat/{}'.format(tag), None)
        return data

# <----Universal Functions---->

    def Register(self):
        Revochat.Welcome()
        print("<<-------------------- Register Account ---------------------->>")
        print("As this is just a simple app for testing purposes, do not use actual credentials for registration" + "\n")
        time.sleep(1)
        name = str(input("Your Name: "))
        username = str(input("Set your username: "))
        password = input("Set a password: ")
        Revochat.writeData(name, "names", 2)
        Revochat.writeData(username, "Usernames", 0)
        Revochat.writeData(password, "Passwords", 1)

        if len(username) or len(password) == 0:
            print("**Enter a valid username and password, one that is not left blank/empty**" + "\n")
            print("--------------->> You will be redirected to Register Account--------->>" + "\n")
            time.sleep(1)
            Revochat.Register()

        elif username.find("@") or username.find(".com") == -1:
            print("The username must be an email" + "\n")
            print("--------------->> You will be redirected to Register Account --------->>" + "\n")
            time.sleep(1)
            Revochat.Register()
        
        elif len(password) < 6:
            print("Your password is too weak! (length < 6 characters)")
            print("--------------->> You will be redirected to Register Account --------->>" + "\n")
            time.sleep(1)

        else:
            time.sleep(1)
            print("**Account successfully created**")
            print("You will be redirected to the login screen")
            Revochat.login()

    def login(self):
        Revochat.Welcome()
        print("<<-------------------- Login Screen ---------------------->>")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        usernames = Revochat.readData("Usernames")
        passwords = Revochat.readData("Passwords")
        if username in usernames and password in passwords:
            time.sleep(1)
            print("**You have successfully logged into your account!**")
            print("You can now begin sending messages to your friends!")
            Revochat.LoadMessages()
            Revochat.SendMessages()
        else:
            time.sleep(1)
            print("Your login credentials do not match the registered credentials")
            Revochat.login()

    def SendMessages(self):
        print("<<-------------------- Revo Messages ---------------------->>")
        sender = str(input("Your Name: "))
        recipient = input("Name of the Recipient: ")
        while True:
            message = input("Enter a message: ")
            if sender and recipient in Revochat.readData("names"):
                context = "{} --> {}".format(sender, recipient )
                message = context + "\n" + message
                Revochat.writeData(message, "messages", 4)
                command = input("Load Messages?(y/N) or exit(e): ")
                if command == "y":
                    Revochat.LoadMessages()
                elif command == "N":
                    Revochat.SendMessages()
                elif command == "e":
                    print("**Thanks for using Revochat, hope to see you later!**") 
                    sys.exit()

    def LoadMessages(self):
        print("<<--------------------------- Your Messages --------------------------->>")
        messages = Revochat.readData("messages")
        for message in messages:
            print(message)
            print("---------------------------------------------------------------------------")


Revochat = Revochat()

database = firebase.FirebaseApplication("https://revochat-78efd.firebaseio.com/", None)
Revochat.getCommand()