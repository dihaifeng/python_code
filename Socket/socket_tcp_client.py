import socket

HOST = '127.0.0.1'
PORT = 34343

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
print("Connect %s:%d OK"%(HOST,PORT))
data = s.recv(1024)
print("Received:",data.decode('utf-8'))
s.close()