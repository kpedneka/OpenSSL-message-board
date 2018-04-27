# OpenSSL-message-board
### Usage
Start the server file:
```
python server.py
```

In a new terminal, start the client:
```
python client.py
```

Initially, the server will prompt the user to input an alphanumeric username and password. After this step, the user can interact with the message board.

At any time, you can use ```ctrl+C``` to stop either the server or the client. If the client is stopped using this method, the server does not leave behind zombie threads.

### Commands
Once the login/sign up is complete on the client side, the client can perform the following operations: 

To get all messages from a server.
```
> GET <group>
```

To post a new message to a group
```
> POST <group> <message>
```

To end a session
```
> END
```

### Design decisions
For this project, we chose:
- To implement our message board using Python. This language makes it really easy to parse language, and the standard libraries allow us to implement almost all the requirements of the project. 
- The SSL Socket library for Python, because it accomplishes a few major objectives while wrapping around the default socket library. It handles encryption and two-way authentication with very little extra work.
- To have the vast majority of client functionality in server.py under the run () function, which is for each client thread. This is because the client program itself actually should not need to know all of the back-end stuff. So the client is only geared with the bare minimum needed to connect and terminate. 
- To store our database in the form of a directory with a named CSV file for each group. This makes it simple to find a particular group, and to just append a user's POST request to the end of the file.
- To use Python's hashlib library. The hashlib library accomplishes SHA-256 hashing. We used that because it made all of our hashing and salting functionality trivial to implement.

### Contributors
- Bruno Lucarelli (bjl145)
- Noel Taide (nvt9)
- Nandan Thakkar (nt248)
- Kunal Pednekar (ksp101)