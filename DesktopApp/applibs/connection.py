import socket
from socket import timeout as TimeoutError
from socket import error as ConnectionError

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5005
DEFAULT_BUFFER_SIZE = 1024
HOST, PORT = 0, 1
CONNECTED = False

CONNECTION = None

NO_ERR, CONN_TIMEOUT_ERR, CONN_REFUSED_ERR, NOT_CONNECTED_ERR = 0, 1, 2, 3

def connect(dest=None):
    global CONNECTED, CONNECTION, NO_ERR, CONN_REFUSED_ERR, CONN_TIMEOUT_ERR
    ERR = NO_ERR
    if dest == None: host, port = DEFAULT_HOST, DEFAULT_PORT
    else: host, port = dest[HOST], dest[PORT]
    try:
        CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONNECTION.connect((host,port))
        CONNECTED = True
    except TimeoutError:
        ERR = CONN_TIMEOUT_ERR
    except ConnectionError:
        ERR = CONN_REFUSED_ERR
    print "ERROR:",ERR
    return ERR

def isConnected():
    global CONNECTED
    return CONNECTED

def sendMessage(msg):
    global CONNECTION, NO_ERR, NOT_CONNECTED_ERR
    ERR = NO_ERR
    data = None
    if isConnected():
        CONNECTION.send(msg)
        ERR = NO_ERR
        data = CONNECTION.recv(DEFAULT_BUFFER_SIZE)
        data = handleMessage(data)
    else:
        ERR = NOT_CONNECTED_ERR
    return (ERR, data)

def handleMessage(msg):
    print("TODO: Handle Message")
    return msg

def closeConnection():
    global CONNECTION, CONNECTED
    if isConnected():
        CONNECTION.close()
        CONNECTED = False
        
if __name__ == "__main__":
    print("IS CONNECTED:", isConnected())
    err = connect()
    if err == NO_ERR:
        print("SENDING MSG:", sendMessage("Hello"))
        print("IS CONNECTED:", isConnected())
    else:
        print("ERROR! %s" % err)
