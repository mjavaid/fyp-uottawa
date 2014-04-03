from socket import *
import thread
import random

import movement as mv
from movement import executeMovement as em

from scanning import scan

BUFF = 1024
HOST = '192.168.1.101' # must be input parameter 
PORT = 5005 # must be input parameter

def response(key):
    return 'Server response: ' + key

def handleScan():
    print "scan"
    scan()
    
def handleMove(ARGS=None):
    print "move"
    if ARGS == None: return
    em([ARGS[1], ARGS[2]])
    print "done"

def handleDisconnect(addr=None):
    print "disconnected:", addr

def handler(clientsock,addr):
    while 1:
        command = clientsock.recv(BUFF)
        command = command.upper()
        ARGS = command.split(" ")
        command = ARGS[0]
        if not command:
            handleDisconnect(addr)
            break
        response = ""
        if command == "GET_DATA_STREAM":
            response = "ACK_GDS"
        elif command == "CLOSE_CONNECTION":
            response = "ACK_CC"
            break
        elif command == "MOVE":
            handleMove(ARGS)
            response = "MOVED"
        elif command == "SCAN":
            handleScan()
            response = "SCANNED"
        else:
            response = str(random.randint(1, 100))+","+str(random.randint(1, 50))
            
        clientsock.send(response)

    clientsock.close()
    print addr, "- closed connection" #log on console

if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    
    mv.enable()
    
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))
    
    mv.disable()

serversock.close()
