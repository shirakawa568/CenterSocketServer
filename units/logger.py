# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   server_log
   Description:
   Author:      shira
   CreateDate:  2020/11/25
-------------------------------------------------
   Change Activity:
                2020/11/25:
-------------------------------------------------
"""
__author__ = 'shira'

import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


class Logger(logging.Logger):

    def __init__(self, name, level='DEBUG', file=None, encoding='utf-8'):
        """
        日志收集器
        :param name:
        :param level:
        :param file:
        :param encoding:
        """
        super().__init__(name)
        # 定义级别
        self.setLevel(level)
        # 定义格式
        sfmt = '%(asctime)s - %(filename)s %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s'
        fmt = logging.Formatter(sfmt)
        # 配置文件输出
        if file:
            file = file + datetime.datetime.now().strftime('%Y-%m-%d.log')
            file_handle = TimedRotatingFileHandler(file, when='D', encoding=encoding, backupCount=10)
            file_handle.setLevel('INFO')
            file_handle.setFormatter(fmt)
            self.addHandler(file_handle)
        # 配置控制台输出
        # 配置颜色
        fmt = logging.Formatter(sfmt)
        handle = logging.StreamHandler()
        handle.setFormatter(fmt)
        self.addHandler(handle)

    # def debug(self, message, *args, **kwargs):
    #     super().debug(f'\033[0;32m{message}\033[0m')
    #
    # def info(self, message, *args, **kwargs):
    #     super().info(f'\033[0;34m{message}\033[0m')
    #
    # def warning(self, message, *args, **kwargs):
    #     super().warning(f'\033[0;37m{message}\033[0m')
    #
    # def error(self, message, *args, **kwargs):
    #     super().error(f'\033[0;31m{message}\033[0m')


if __name__ == '__main__':
    log = Logger('log', file='..\\')
    log.info('level-info')
