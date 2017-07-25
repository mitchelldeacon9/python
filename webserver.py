#!/usr/bin/python
# this scripts implements a simple webserver to reply to GET requests 
# webserver binds to port 3000 and serves files in current directory

import socket
import os
from os import curdir

dir = os.listdir(os.curdir)
serverAddr = '127.0.0.1'
port = 3000
print('starting on %s , listening on port %d' % (serverAddr, port))

print ''
print dir
print ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((serverAddr, port))
s.listen(1)

while 1:
    connection, clientAddr = s.accept()
    data = connection.recv(1024)
    if data:
        print('received "%s"' % data)
        dataList = data.split(' ')
        x = dataList[1]
        file = '/' + x

        try:
            f = open(curdir + file)
        except IOError:
            connection.sendall('HTTP/1.1 404\nContent-type: text/plain\n\n404 File Not Found')
        else:
            connection.sendall('HTTP/1.1 200 OK\n')
            connection.sendall('Content-type: text/plain\nConnection: close\n\n')
            connection.sendall(f.read())
            f.close()
        finally:
            connection.close()
