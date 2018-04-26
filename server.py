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
                # search for username, store hash in variable 'password'

                while valid_password is False:
                    msg = 'Please enter an alphanumeric password'
                    self.client_ssl.send(bytes(msg.encode('UTF-8')))
                    data = self.client_ssl.recv(2048)
                    password = data.decode()
                    if password.isalnum() is True:
                        valid_password = True
                correct_password = False
                while correct_password is False:
                    hashed_pass_str = getHashedPass(username)
                    # if username doesn't yet exist, add it to the password file
                    if hashed_pass_str is None:
                        addUserPass(username, password)
                        correct_password = True
                    # else, hash the password with the salt and see it matches the result
                    else:
                        # if they match, authenticate
                        hash_obj = hashlib.sha256()
                        hash_obj.update(oursalt + password)
                        attempted_hash_str = hash_obj.hexdigest()
                        print "attempted hash str: " + attempted_hash_str + "\n"
                        print "actual hash str: " + hashed_pass_str + "\n"
                        if attempted_hash_str == hashed_pass_str:
                            correct_password = True
                        # otherwise, tell the user
                        else:
                            msg = 'Error: invalid password.'
                            print "Client entered invalid password.\n"
                            self.client_ssl.send(bytes(msg.encode('UTF-8')))
                            break

                if correct_password is True:
                    auth = True
                print("User ", username, " entered password ", password)


            msg = "Welcome, " + username
            self.client_ssl.send(bytes(msg.encode('UTF-8')))

            while True:
                data = self.client_ssl.recv(2048)
                msg = data.decode()
                if msg == 'END':
                    self.client_ssl.send(bytes("Connection closed".encode('UTF-8')))
                    break
                if msg.split()[0] not in ['GET','POST'] or len(msg.split()) <= 1:
                    self.client_ssl.send(bytes("Invalid operation.".encode('UTF-8')))
                msg = msg.split()
                print msg
                if msg[0] == "GET":
                    messages = api.get_messages(msg[1])
                    messages = api.get_messages(msg[1])
                    self.client_ssl.send("these are the messages in the group".join(messages).encode('UTF-8'))
                    print "these are the messages in the group", messages
                if msg[0] == "POST":
                    api.put_messages(msg[1],username, msg[2])
                self.client_ssl.send(bytes("".join(msg).encode('UTF-8')))
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
    with open('passwords.txt', 'r+') as pass_file:
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