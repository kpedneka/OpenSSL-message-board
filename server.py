import socket, threading, os, ssl, hashlib
import api

oursalt = "thisisourprojectssalt"

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, client_ssl):
        threading.Thread.__init__(self)
        self.client_ssl = client_ssl
        self.kill_received = False
        print ("New connection added: ", clientAddress)

    def run(self):
        while not self.kill_received:
            print ("Connection from : ", clientAddress)
            auth = False
            valid_user = False
            valid_password = False

            # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
            while auth is False:
                while valid_user is False:
                    msg = 'Please enter an alphanumeric username'
                    self.client_ssl.send(bytes(msg.encode('UTF-8')))
                    data = self.client_ssl.recv(2048)
                    username = data.decode()
                    if username.isalnum() is True:
                        valid_user = True

                print("User entered username: ", username)
                hashed_pass_str = getHashedPass(username)
                if hashed_pass_str is None:
                    #User does not exist. Create account
                    while valid_password is False:
                        msg = 'New user ' + username + ', please enter an alphanumeric password'
                        self.client_ssl.send(bytes(msg.encode('UTF-8')))
                        data = self.client_ssl.recv(2048)
                        password = data.decode()
                        if password.isalnum() is True:
                            addUserPass(username, password)
                            valid_password = True
                            auth = True
                    break

                # User does exist. Authenticate with password
                # retrieve user's correct password from file
                hashed_pass_str = getHashedPass(username)
                correct_password = False
                first_run = True  # used to check whether we send "Enter your password" vs. "error: wrong password"
                while correct_password is False:
                    if first_run:
                        msg = 'User ' + username + ', please enter your password'
                        self.client_ssl.send(bytes(msg.encode('UTF-8')))
                        first_run = False
                    # receive password attempt from user
                    password = self.client_ssl.recv(2048).decode()

                    # if hashed attempt matches retrieved hash, authenticate
                    hash_obj = hashlib.sha256()
                    hash_obj.update(oursalt + password)
                    attempted_hash_str = hash_obj.hexdigest()
                    print "attempted hash str: " + attempted_hash_str + "\n"
                    print "actual hash str: " + hashed_pass_str + "\n"
                    if attempted_hash_str == hashed_pass_str:
                        correct_password = True
                    # otherwise, tell the user
                    else:
                        msg = 'Error: Incorrect password. Try again'
                        print "Client entered incorrect password.\n"
                        self.client_ssl.send(bytes(msg.encode('UTF-8')))
                        #break

                if correct_password is True:
                    auth = True
                print("User ", username, " entered password ", password)

            msg = 'Welcome, ' + username + '! List of groups: ' + ' '.join(api.get_groups())
            self.client_ssl.send(bytes(msg.encode('UTF-8')))
            while True:
                data = self.client_ssl.recv(2048)
                msg = data.decode()
                if msg == 'END':
                    self.client_ssl.send(bytes("Connection closed".encode('UTF-8')))
                    break
                if msg.split()[0] not in ['GET','POST'] or len(msg.split()) <= 1:
                    self.client_ssl.send(bytes("Invalid operation.".encode('UTF-8')))
                msg = msg.split(' ', 2)
                print msg
                if len(msg) > 1:
                    if msg[0] == "GET":
                        messages = api.get_messages(msg[1])
                        #self.client_ssl.send("these are the messages in the group".join(messages).encode('UTF-8'))
                        if len(messages) > 0:
                            messages_string = ''.join(messages)
                            self.client_ssl.send(bytes(messages_string.encode('UTF-8')))
                            print "these are the messages in the group", messages
                        else:
                            self.client_ssl.send(bytes("No messages found for that group".encode('UTF-8')))
                    elif msg[0] == "POST":
                        if len(msg) > 2:
                            api.put_messages(msg[1],username, msg[2])
                            self.client_ssl.send(bytes(("POST received for message: " +
                                                        "\"" + msg[2] + "\"").encode('UTF-8')))
                        else:
                            self.client_ssl.send(bytes("Please enter a message to POST".encode('UTF-8')))
                    else:
                        self.client_ssl.send(bytes("Invalid operation.".encode('UTF-8')))
                #self.client_ssl.send(bytes("".join(msg).encode('UTF-8')))
            self.kill_received = True
            print ("Client at ", clientAddress, " disconnected...")

def getHashedPass(username):
    # open the passwords.txt (create it if not present)
    with open('passwords.txt', 'a+') as pass_file:
    # search line by line
        # for each line, split the user and password hash by a semicolon
        line_list = pass_file.readlines()
        for line in line_list:
            split = line.strip().split(":")
            curr_username = split[0]
            curr_pass_hash_str = split[1]
            print "checking username: " + curr_username + "\n"
            print "checking hashed password: " + curr_pass_hash_str + "\n"
            # once the username matches input username, return password hash
            if curr_username == username:
                print "found username!\n"
                pass_file.close()
                return curr_pass_hash_str
    # we haven't returned anything, return null
    pass_file.close()
    return None

def addUserPass(username, password):
    # open the passwords.txt (create it if not present)
    with open('passwords.txt', 'a') as pass_file:
        # hash the password with pass_salt, SHA-256
        hash_obj = hashlib.sha256()
        hash_obj.update(oursalt + password)
        hashed_pass_str = hash_obj.hexdigest()
        # add a line with username and hashed password, separated by only a semicolon
        print "adding username: " + username + "\n"
        print "for hashed pass: " + hashed_pass_str + "\n"
        new_line = username + ":" + hashed_pass_str + "\n"
        pass_file.write(new_line)


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
threads = []
while True:
    try:
        server.listen(1)
        client_sock, clientAddress = server.accept()
        # wrap client's socket for SSL
        client_ssl = ssl.wrap_socket(client_sock,
                                     server_side=True,
                                     certfile="server.crt",
                                     keyfile="server.key")
        newthread = ClientThread(clientAddress, client_ssl)
        newthread.start()
        threads.append(newthread)
    except KeyboardInterrupt:
        print "Interrupted"
        for t in threads:
            t.kill_received = True
            t.client_ssl.send(bytes("CLOSE".encode('UTF-8')))
            print(t.getName(), "Closed")
        os._exit(0)