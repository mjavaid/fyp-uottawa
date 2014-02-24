#!/usr/bin/env python

import socket
import re


def sep (str):
	received_file = open("received_file.txt", "a") 
	
	print "str.replace" 
	str =str.replace(',','\n')
	print str
	#pattern =''
	str=re.sub(r"[\['\]]",'',str) #remove all "[","]"," ' "
	print "str.sub" 
	print str
	
	received_file.write(str.replace(',','\n'))
	
	received_file.close()



HOST = 'localhost' #localhost 
PORT = 5005

BUFFER_SIZE = 1024


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
        	sep(data)
        	#received_file.write(str(data)) # add to the file
        	#received_file.close()
        	print("Reply: "),data
        elif c == MESSAGE:
        	print "server closed"
        	break
         


      
#received_file.close()
s.close()


