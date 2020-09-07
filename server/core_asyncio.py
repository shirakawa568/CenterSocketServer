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

import socket
import asyncio
from threading import Thread


class SocketServer:

    def __init__(self, ip, port):
        """
        初始化SOCKET服务
        """
        # self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss = None
        self.dict_fd = dict()
        asyncio.run(self.start(ip, port))

    async def start(self, ip, port):
        server = await asyncio.start_server(self.handler, ip, port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    async def handler(self, reader, writer):
        data = await reader.read()
        message = data.decode()
        if message == '':
            print("Close the connection")
            writer.close()
        else:
            addr = writer.get_extra_info('peername')

            print(f"Received {message!r} from {addr!r}")

            print(f"Send: {message!r}")
            writer.write(data)
            await writer.drain()

        # print("Close the connection")
        # writer.close()

    @staticmethod
    def auto_result(sock):
        sock.send('ok'.encode())


