#!/usr/bin/env python

import socket
import re


def sep (string):
	received_file = open("received_file.txt", "a") 
	
	print "string"
	print string 
	

	
	print "string2"
	print string 
	
	
	string =string.replace(',','\n')
	#print string
	#pattern =''
	string=re.sub(r" [']",'',string) #remove all " " after '
	string=re.sub(r"[\['\]-]",'',string) #remove all "[","]"," ' "

	print "string.sub" 
	print string
	
	received_file.write(string)
	
	received_file.close()
	return string


HOST = 'localhost' #localhost 
PORT = 5005

BUFFER_SIZE = 10000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT)) #double (()) coz connect takes 1 para

#s.send("Hello im connected")


while 1:
		
        MESSAGE = raw_input("Ur message: ")
        c = "close"
        print "ENTERED: ", MESSAGE
        
        if MESSAGE == "":
        	print "No Data Entered"
      
      
        elif MESSAGE != c:
        	#received_file = open("received_file.txt", "a") 
    
        	s.send(MESSAGE)
        	print ("waiting...")
        	data = s.recv(BUFFER_SIZE)
        	string=sep(data)
        	#received_file.write(string(data)) # add to the file
        	#received_file.close()
        	print"Reply: "+string
        elif c == MESSAGE:
        	print "server closed"
        	break

#received_file.close()
s.close()