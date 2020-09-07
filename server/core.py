# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   core
   Description:
   Author:      shira
   CreateDate:  2020/8/31
-------------------------------------------------
   Change Activity:
                2020/8/31:
-------------------------------------------------
"""
__author__ = 'shira'

import gevent
from gevent import socket, monkey

monkey.patch_all(thread=False)


class SocketServer:

    def __init__(self, ip, port):
        """
        初始化SOCKET服务
        """
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((ip, port))
        self.ss.listen(5)
        self.dict_fd = dict()
        self.start()

    def start(self):
        print(self.ss.getsockname())
        while True:
            sock, addr = self.ss.accept()
            self.dict_fd[sock.fileno()] = sock
            # 通过gevent启动一个协程
            gevent.spawn(self.handler, sock)

    def handler(self, sock: socket):
        while True:
            data = sock.recv(1024)
            if data == b'':
                sock.close()
                break
            print(data.decode())
            self.auto_result(sock)
            self.send_all(sock, data.decode())

    @staticmethod
    def auto_result(sock):
        sock.send('ok'.encode())

    @staticmethod
    def sendto(sock, msg):
        sock.send(msg.encode())

    def send_all(self, sock_self, msg):
        for fd, sock in self.dict_fd.items():
            if sock is not sock_self:
                # 通过gevent启动一个协程
                gevent.spawn(self.sendto, sock, msg)
