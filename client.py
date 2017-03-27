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
from gevent.event import AsyncResult

MAX_REQUEST_ID = 100


class Client(ServerService):
    def __init__(self):
        ServerService.__init__(self)
        self.stubs = {} # 供长连接使用
        self.next_id = 0


    def get_request_id(self):
        nid = self.next_id
        if nid == MAX_REQUEST_ID:
            nid = 0
        nid += 1
        self.next_id = nid
        return nid


    def _call_method(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 63003))
        conn = net.tcp.Connection(sock, None)
        channel = Channel(conn, self, ServerService_Stub)
        req = CallRequest()
        req.request_id = self.get_request_id()
        req.method = '1.B'
        req.parameters = json.dumps({'test': 23})
        result = AsyncResult()
        self.replies[req.request_id] = result
        channel.stub.call_method(None, req)
        return result.get()


    def call(self, method, kwargs, timeout=None, callback=None):
        '''
        阻塞调用call
        :param method: 方法名(str)，
        :param kwargs: 参数字典(dict)
        :timeout: 超时
        :param callback: 不需要设置
        :return: 远程rpc的返回值
        '''
        return



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
    print client._call_method()
    client = Client()
    print client._call_method()

