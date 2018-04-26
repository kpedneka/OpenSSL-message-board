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


### Commands
To get all messages from a server
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