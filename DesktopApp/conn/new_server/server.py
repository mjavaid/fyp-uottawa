from socket import *
import threading
import thread

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFSIZ)
        
        if not data: #client closed the server
            print "Client:" + str(addr) + '....Left'
            break
        msg = 'massage: ' + data
        
        print "Client:" + str(addr) + 'Says: '+ data
        
        if data =="all":
        	text_file = open("dumpfile.txt", "r") 
        	lines =text_file.readlines()
        	lines= [item.rstrip() for item in lines] # take out the \n
        	
        	clientsock.send(str(lines)+"\n")
        	
        
        elif data =="point":
          for line in text_file:
          	pass
          clientsock.send(line+"\n")	
          
        else:
        	clientsock.send(data+"\n")
        	
        
       
        #clientsock.send(msg)
        if "close" == data.rstrip(): # type 'close' on client console to close connection from the server side
        	clientsock.close()
        	break
    clientsock.close()





if __name__=='__main__':
    HOST = 'localhost'
    PORT = 5005
    BUFSIZ = 10000
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(2)
    
    text_file = open("dumpfile.txt", "r") 
    print 'Server is running'
    while 1:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print 'Connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))