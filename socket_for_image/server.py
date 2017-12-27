#!/usr/bin/env python
# -*- coding=utf-8 -*-
import socket
import threading
import time
import sys
import os
import struct

def tcplink(sock, addr):
    print('Accept new connection from %s: %s' % addr)
    sock.send(b'Hi, Welcome to the server!')

    fileinfo_size = struct.calcsize('128sl')
    buf = sock.recv(fileinfo_size)
    if buf:
        filename, filesize = struct.unpack('128sl', buf)
        fn = filename.decode().strip('\00') #将编码时产生的多余的\00去除
        new_filename = 'new' + fn

        recv_size = 0 #已接受文件大小
        f = open(new_filename, 'wb')
        while not recv_size == filesize:
            if filesize - recv_size >1024:
                data = sock.recv(1024)
                recv_size = recv_size + len(data)
            else:
                data = sock.recv(filesize - recv_size)
                recv_size = filesize
            f.write(data)
        f.close()
        
    sock.close()


def server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 9999))
        s.listen(5)
        print('Waiting connection...')
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
        print("waiting for connecting")

if __name__ == "__main__":
    server()