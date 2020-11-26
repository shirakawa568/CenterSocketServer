# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   verification
   Description:
   Author:      shira
   CreateDate:  2020/11/25
-------------------------------------------------
   Change Activity:
                2020/11/25:
-------------------------------------------------
"""
__author__ = 'shira'

import json
from json import JSONDecodeError


def message_verify(message):
    """
    消息格式验证
    :param message: str 接受的消息
    :return:
    """
    try:
        dict_ = json.loads(message)
        if dict_.get('cmdType') is None:
            raise Exception('Missing parameter cmdType')
        if dict_.get('cmdData') is None:
            raise Exception('Missing parameter cmdData')
        if dict_.get('sendTime') is None:
            raise Exception('Missing parameter sendTime')
        if dict_.get('sendUser') is None:
            raise Exception('Missing parameter sendUser')
        if dict_.get('recvType') is None:
            raise Exception('Missing parameter recvType')
        else:
            recvType = dict_.get('recvType')
            if recvType == 'user':
                if dict_.get('recvUser') is None:
                    raise Exception('Missing parameter recvUser')
            elif recvType == 'group':
                if dict_.get('recvGroup') is None:
                    raise Exception('Missing parameter recvGroup')
            else:
                raise Exception('recvType is Illegal parameters')

        # 数据验证成功
        response = True, dict_
    except JSONDecodeError as e:
        response = False, f'非JSON格式字符串：{e}'
    except Exception as e:
        response = False, f'参数错误：{e}'
    return response


def simple_auth(cmd):
    """
    简单身份验证：
        只验证身份类型、客户端名称，使socket易于辨识；
        注：无密码验证
    :param cmd:
    :return:
    """
    client_type_list = (0,)
    try:
        cmdDate = cmd.get('cmdDate', None)
        if not cmdDate:
            raise Exception("Null parameter")
        client_type = cmdDate.get('clientType')
        client_name = cmdDate.get('clientName')

        if client_type not in client_type_list:
            raise Exception("clientType is Illegal parameters")

        return True, client_type, client_name
    except Exception as e:
        return e


if __name__ == '__main__':
    data = {
        "cmdType": 1,
        "cmdData": "",
        "sendTime": "",
        "sendUser": "",
    }
    print(message_verify(json.dumps(data)))
