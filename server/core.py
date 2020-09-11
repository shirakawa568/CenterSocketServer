# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   core
   Description: 服务端核心代码
                包括：
                    服务端的启动；
                    客户端的监听；
                    消息接受与预处理；
                    消息分发；
                    群组维护与管控；
                        每个被控端，使用独立的群组；
                        控制端只能加入已存在的群组；
   Author:      shira
   CreateDate:  2020/8/31
-------------------------------------------------
   Change Activity:
                2020/8/31:
                2020/9/10: 增加模块描述
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
