import socket, threading, os


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.kill_received = False
        print ("New connection added: ", clientAddress)

    def run(self):
        while not self.kill_received:
            print ("Connection from : ", clientAddress)
            # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
            msg = ''
            while True:
                data = self.csocket.recv(2048)
                msg = data.decode()
                if msg == 'quit':
                    break
                print ("from client", msg)
                self.csocket.send(bytes(msg.encode('UTF-8')))
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
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()
        threads.append(newthread)
    except KeyboardInterrupt:
        print("Interrupted")
        for t in threads:
            t.kill_received = True
            t.csocket.send(bytes("CLOSE".encode('UTF-8')))
            print(t.getName(), "Closed")
        os._exit(0)