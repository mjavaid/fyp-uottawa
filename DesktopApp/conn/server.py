#!/usr/bin/env python 

import socket


TCP_IP = '' #localhost 
TCP_PORT = 5005

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT)) #double (()) coz connect takes 1 para
s.listen(1) # how many connections it can receive at one time
print ("Server is running....!")
conn, addr = s.accept() # accept the connection 

print ("Connection address:"), addr #print the address of the client 


while 1:
    
    data = conn.recv(BUFFER_SIZE) # recives datae (1024 bytes) using conn and store into data 
 
    if not data: break
   
    print ("received data: "), data # print data; Data is the message the users types
    reply = raw_input("Reply: ")
    conn.sendall(reply)  # send all will send to all client connected 
    
conn.close()
