import socket

HOST = '127.0.0.1'
PORT = 3434

# AF_INET 说明是IPv4地址；SOCK_DGRAM指明是UDP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

data = "Hello,UDP!"
print(data)

s.sendto(data.encode('utf-8'),(HOST,PORT))
print("Sent: %s to %s:%d" %(data,HOST,PORT))

s.close()