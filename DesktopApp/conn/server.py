from socket import *
import thread
import random

import argparse

BUFF = 1024
HOST = 'localhost'# must be input parameter 
PORT = 5005 # must be input parameter

def response(key):
    return 'Server response: ' + key

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)
        if not data: break
        print repr(addr) + ' recv:' + repr(data)
        response = ""
        if data == "GET_DATA_STREAM":
            response = "ACK_GDS"
        elif data == "CLOSE_CONNECTION":
            response = "ACK_CC"
            break
        else:
            response = str(random.randint(1, 100))+","+str(random.randint(1, 50))
            
        clientsock.send(response)
        print repr(addr) + ' sent:' + repr(data)

        if "CLOSE_CONNECTION" == data: break

    clientsock.close()
    print addr, "- closed connection" #log on console

if __name__=='__main__':
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        print 'waiting for connection... listening on port', PORT
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))

serversock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config', help='Server configuration file')
    args = parser.parse_args()
