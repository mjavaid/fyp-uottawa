from errno import ECONNREFUSED as ConnectionRefusedError
import socket
from socket import timeout as TimeoutError

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5004
DEFAULT_BUFFER_SIZE = 1024
HOST, PORT = 0, 1
CONNECTED = False

CONNECTION = None

NO_ERR, CONN_TIMEOUT_ERR, CONN_REFUSED_ERR, NOT_CONNECTED_ERR = 0, 1, 2, 3

def connect(dest=None):
    ERR = NO_ERR
    if dest == None: host, port = DEFAULT_HOST, DEFAULT_PORT
    else: host, port = dest[HOST], dest[PORT]
    try:
        CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONNECTION.connect((host,port))
        CONNECTED = True
    except TimeoutError:
        ERR = CONN_TIMEOUT_ERR
    except socket.ConnectionRefusedError:
        ERR = CONN_REFUSED_ERR
    return ERR
    print("TODO: Connect")

def isConnected():
    return CONNECTED

def sendMessage(msg):
    ERR = NO_ERR
    if isConnected():
        CONNECTION.send(bytes(msg, 'UTF-8'))
        ERR = NOT_ERR
    else:
        ERR = NOT_CONNECTED_ERR
    return ERR
    print("TODO: Send Message")

def handleMessage(msg):
    print(msg)
    print("TODO: Handle Message")

"""class CONN:
    conn = None
    connected = False
    NO_ERR = 0
    CONN_TIMEOUT_ERR = 1
    CONN_REFUSED_ERR = 2
    NOT_CONNECTED_ERR = 4
    
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connectToRobot(self, ARGS):
        ERR = self.NO_ERR
        host, port = None, None
        if ARGS[HOST]==None: host = DEFAULT_HOST
        else: host = ARGS[HOST]
        if ARGS[PORT]==None: port = DEFAULT_PORT
        else: port = ARGS[PORT]
        try:
            self.conn.connect((host, port))
            self.connected = True
        except TimeoutError:
            ERR = self.CONN_TIMEOUT_ERR
        except ConnectionRefusedError:
            ERR = self.CONN_REFUSED_ERR
        return ERR
    
    def isConnected(self):
        return self.connected
    
    def sendMessage(self, msg):
        ERR = self.NO_ERR
        if self.isConnected():
            self.conn.send(bytes(msg, 'UTF-8'))
        else: ERR = self.NOT_CONNECTED_ERR
        return ERR"""
        
if __name__ == "__main__":
    """connection = CONN()
    print(connection.connectToRobot())
    print(connection.isConnected())
    print(connection.sendMessage("Hello"))
    
    print("IS CONNECTED:", isConnected())
    print("CONNECTING:", connect())
    print("SENDING MSG:", sendMessage("Hello"))
    print("IS CONNECTED:", isConnected())"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DEFAULT_HOST, DEFAULT_PORT))
    while True:
        command = raw_input('Enter your command: ')
        print 'CMD:', command
        if (command.split(' ',1))[0] == 'STORE':
            print 'CMD STORE!'
            while True:
                additional_text = raw_input()
                command = command + '\n' + additional_text
                if additional_text == '.': break
        s.send(command)
        print 'SENT:', command
        reply = s.recv(1024)
        print 'RECEIVED!'
        if reply == 'Quit': break
        print reply

