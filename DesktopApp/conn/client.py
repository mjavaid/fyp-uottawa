#!/usr/bin/env python

import socket


TCP_IP = 'localhost' #localhost 
TCP_PORT = 5005

BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT)) #double (()) coz connect takes 1 para

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
        	print("Reply: "),data
        elif c == MESSAGE:
        	print "server closed"
        	break
	
s.close()


