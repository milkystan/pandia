#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 15:31
# @Author  : Stan
# @File    : client.py

import gevent
from net.proto_python.server_pb2 import ServerService_Stub, CallRequest
from gevent import socket
from net.channel import *
import net.tcp
import json
from service import ServerService

gl = None

class Client(object):
    def __init__(self):
        self.server_stub = None

    def _call_method(self):
        global gl
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 63000))
        conn = net.tcp.Connection(sock, None)
        channel = Channel(ServerService(None), conn)
        gl = channel
        stub = ServerService_Stub(channel)
        req = CallRequest()
        req.request_id = 1
        req.method = '1.B'
        req.parameters = json.dumps({'test': 23})
        stub.call_method(None, req)

    def call(self, method, kwargs, timeout=None, callback=None):
        '''
        阻塞调用call
        :param method: 方法名， 检查合法性
        :param kwargs: 参数字典 ，检查合法性
        :timeout: 超时
        :param callback: 不需要设置
        :return: 远程rpc的返回值
        '''
        pass



    def cast(self, method, kwargs, timeout=None, callback=None):
        '''
        阻塞调用cast
        :param method: 方法名
        :param kwargs: 参数字典
        :timeout: 超时
        :param callback: 不需要设置
        :return: None
        '''
        pass

    def async_call(self, method, kwargs, timeout=None, callback=None):
        '''
        异步调用call
        :param method: 方法名
        :param kwargs: 参数字典
        :timeout: 超时
        :param callback: 回调函数
        :return: Greenlet对象
        '''
        return gevent.spawn(self.call, method, kwargs, timeout=None, callback=callback)

    def async_cast(self, method, kwargs, callback=None):
        '''
        异步调用cast
        :param method: 方法名
        :param kwargs: 参数字典
        :timeout: 超时
        :param callback: 回调函数
        :return: Greenlet对象
        '''
        return gevent.spawn(self.cast, method, kwargs, callback=callback)


if __name__ == '__main__':
    client = Client()
    client._call_method()
    while True:
        gevent.sleep(0)
