import socket, threading, os, ssl


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, client_ssl):
        threading.Thread.__init__(self)
        self.client_ssl = client_ssl
        self.kill_received = False
        print ("New connection added: ", clientAddress)

    def run(self):
        while not self.kill_received:
            print ("Connection from : ", clientAddress)
            auth = False;
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
                        valid_user = True;

                print("User entered username: ", username)
                # search for username, store hash in variable 'password'

                while valid_password is False:
                    msg = 'Please enter an alphanumeric password'
                    self.client_ssl.send(bytes(msg.encode('UTF-8')))
                    data = self.client_ssl.recv(2048)
                    password = data.decode()
                    if password.isalnum() is True:
                        valid_password = True;

                auth = True
                print("User ", username, " entered password ", password)

                # if password is null, user must create account by entering password

                # if password is not null, ask user to enter password, hash, and compare against our checked hash

            msg = "Welcome, " + username
            self.client_ssl.send(bytes(msg.encode('UTF-8')))

            while True:
                data = self.client_ssl.recv(2048)
                msg = data.decode()
                if msg == 'quit':
                    break
                print("from client", msg)
                self.client_ssl.send(bytes(msg.encode('UTF-8')))
            self.kill_received = True
            print ("Client at ", clientAddress, " disconnected...")


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