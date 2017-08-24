#!/usr/bin/python3           # This is server.py file
import socket                                         

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 
                   

port = 9999                                           

# bind to the port
serversocket.bind(('', port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))
    print(clientsocket.recv(1024))
   
    clientsocket.close()