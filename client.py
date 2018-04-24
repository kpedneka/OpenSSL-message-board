import socket, ssl

SERVER = "127.0.0.1"
PORT = 8080
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_ssl = ssl.wrap_socket(client_sock,
                             ca_certs="server.crt",
                             cert_reqs=ssl.CERT_REQUIRED)
client_ssl.connect((SERVER, PORT))
client_ssl.sendall(bytes("This is from Client".encode("UTF-8")))
while True:
    in_data = client_ssl.recv(1024)
    if in_data == 'CLOSE':
        break
    print("From Server :", in_data.decode())
    out_data = raw_input()
    client_ssl.sendall(bytes(out_data.encode("UTF-8")))
    if out_data == 'quit':
        break
print "Closing connection"
client_ssl.close()
