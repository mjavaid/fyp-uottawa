import socket

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 80
DEFAULT_BUFFER_SIZE = 1024
HOST, PORT = 0, 1

class CONN:
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
        return ERR
        
if __name__ == "__main__":
    connection = CONN()
    print(connection.connectToRobot())
    print(connection.isConnected())
    print(connection.sendMessage("Hello"))
