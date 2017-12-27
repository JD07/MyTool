#!/usr/bin/env python
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct

def client():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 9999))
        print(sock.recv(1024).decode)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
   

    while True:
        filepath = input('please input file path: ')
        if os.path.isfile(filepath):
            #定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            #定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath).encode(), os.stat(filepath).st_size)
            #将文件名和文件大小发送给服务器
            sock.send(fhead)
            print('client filepath: %s' % filepath)

            #发送图片
            f = open(filepath, 'rb') #以二进制形式打开
            while True:
                data = f.read(1024)
                if not data:
                    print("image send over")
                    break
                sock.send(data)

        sock.close()
        break

if __name__ == "__main__":
    client()