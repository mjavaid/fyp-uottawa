import socket

s = socket.socket()
s.connect((ip,port))
s.send("my request\r")
print s.recv(256)
s.close()