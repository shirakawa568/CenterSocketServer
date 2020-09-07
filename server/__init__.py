# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   __init__.py
   Description:
   Author:      shira
   CreateDate:  2020/8/31
-------------------------------------------------
   Change Activity:
                2020/8/31:
-------------------------------------------------
"""
__author__ = 'shira'

from server import core_asyncio, core


def create_server(ip, port):
    # return core_asyncio.SocketServer(ip, port)
    return core.SocketServer(ip, port)

# server = create_server('', '')
