import socket

HOST = '0.0.0.0'
PORT = 3434

# AF_INET 说明是IPv4地址；SOCK_DGRAM指明是UDP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data, addr = s.recvfrom(1024)
    print("Received: %s from %s" % (data.decode('utf-8'),str(addr)))

s.close()