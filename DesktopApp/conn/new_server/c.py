#!/usr/bin/env python

import socket


HOST = 'localhost' #localhost 
PORT = 5005

BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT)) #double (()) coz connect takes 1 para

#s.send("Hello im connected")

received_file = open("received_file.txt", "a") 
while 1:
		
        MESSAGE = raw_input("Ur message: ")
        c = "close"
        print "ENTERED: ", MESSAGE
        
        if MESSAGE == "":
        	print "No Data Interd"
        elif MESSAGE != c:
        	s.send(MESSAGE)
        	print ("watting...")
        	data = s.recv(BUFFER_SIZE)
        	received_file.write(str(data)) # add to the file
        	
        	print("Reply: "),data
        elif c == MESSAGE:
        	print "server closed"
        	break
         
        
received_file.close()
s.close()


