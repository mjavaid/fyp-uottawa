from socket import *
import thread

BUFF = 1024
HOST = 'localhost'# must be input parameter 
PORT = 5005 # must be input parameter

i = 0

def response(key):
    return 'Server response: ' + key

def handler(clientsock,addr):
    global i
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
            response = str(i)+","+str(i*5)
            
        clientsock.send(response)
        print repr(addr) + ' sent:' + repr(data)

        if "CLOSE_CONNECTION" == data: break
        i += 1
    i = 0
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
