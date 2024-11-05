import socket

s = socket.socket()
host = socket.gethostname()
port = 1717
s.bind((host, port))
#Use gethostbyname
host = socket.gethostbyname("192.168.1.2")
s.bind((host, port))
