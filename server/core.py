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

import datetime
import time

import gevent
from gevent import socket, monkey

from server.constant import DEFAULT_GROUP_ID
from server.extensions import *
from server.verification import *

monkey.patch_all(thread=False)


class SocketServer:

    def __init__(self, ip, port):
        """
        初始化SOCKET服务
        """
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((ip, port))
        self.ss.listen(10)
        self.dict_fd = dict()
        self.start()

    def start(self):
        logging.info(self.ss.getsockname())
        while True:
            sock, addr = self.ss.accept()
            self.dict_fd[sock.fileno()] = sock
            logging.info(f'{sock.fileno()}接入, 连接数：{len(self.dict_fd)}')
            self.sendto(sock, 'success')
            sock.create_time = time.time()
            # 通过gevent启动一个协程
            gevent.spawn(self.handler, sock)

    def handler(self, sock: socket):
        """
        监听客户端消息
        :param sock:
        :return:
        """
        try:
            while not sock.closed:
                data = sock.recv(9999999)
                if not data:
                    # 处理正常推出的sock
                    logging.info(f'{sock.fileno()} 离开了')
                    del self.dict_fd[sock.fileno()]
                    sock.close()
                    break
                logging.debug(f'来自：{sock.fileno()} - {data.decode()}')
                # 验证指令格式，格式错误将忽略指令
                res = message_verify(data.decode())
                if not res[0]:
                    logging.error(f'{sock.fileno()} - {res[1]}')
                    self.sendto(sock, res[1])
                    continue

                # 身份验证
                if res[1].get('cmdType') == 'clientLogin':
                    res = simple_auth(res[1].get('cmdDate'))
                    if res[0]:
                        sock.is_login = True
                        # todo：分配群组
                        sock.group = DEFAULT_GROUP_ID  # 默认群组

                # 未登录状态判断
                if not sock.is_login:
                    if sock.create_time - time.time() > 10:

                        sock.close()

                    continue

                # 即时通讯 instantMessaging
                if res[1].get('cmdType') == 'instantMessaging':
                    res = simple_auth(res[1].get('cmdDate'))

                # todo：

                # 连接成功回复
                # self.auto_result(sock)
                # 转发其他客户端
                # self.send_all(sock, data.decode())
        except ConnectionResetError as e:
            logging.error(f'{sock.fileno()} 异常断开：{e}')
            del self.dict_fd[sock.fileno()]
            sock.close()
        except ConnectionAbortedError as e:
            logging.error(f'{sock.fileno()} 异常断开：{e}')
            del self.dict_fd[sock.fileno()]
            sock.close()
        except OSError as e:
            logging.error(f'{sock.fileno()} 异常断开：{e}')
            del self.dict_fd[sock.fileno()]
            sock.close()
        except Exception as e:
            logging.error(f'{sock.fileno()} 严重异常断开，请管理员注意：{e}')
            del self.dict_fd[sock.fileno()]
            sock.close()

    @staticmethod
    def auto_result(sock):
        sock.send('ok'.encode())

    @staticmethod
    def heart_beat(sock):
        sock.send(f'{datetime.datetime.now()}-ok'.encode())

    @staticmethod
    def sendto(sock, msg):
        sock.send(msg.encode())

    def send_all(self, sock_self, msg):
        for fd, sock in self.dict_fd.items():
            if sock is not sock_self:
                # 通过gevent启动一个协程
                gevent.spawn(self.sendto, sock, msg)
