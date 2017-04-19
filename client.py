#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 15:31
# @Author  : Stan
# @File    : client.py

import gevent
from net.proto_python.server_pb2 import ServerService_Stub, CallRequest, ChannelInfo
from gevent import socket
from net.channel import *
import net.tcp
import json
from rpc_service import ServerService
from gevent.event import AsyncResult

MAX_REQUEST_ID = 100


class Client(ServerService):
    '''
    相较ChannelClient，加入一些cache
    '''
    def __init__(self, is_server=False, cache_time=None):
        '''
        :param is_server: 是否是Server端创建的Client对象
        :param cache_time: 缓存保留时间，单位：秒
        :return:
        '''
        ServerService.__init__(self)
        # 供长连接使用
        self.stubs = {}
        self.next_id = 0
        self.is_server = is_server
        self.cache_time = cache_time

    def get_request_id(self):
        nid = self.next_id
        if nid == MAX_REQUEST_ID:
            nid = 0
        nid += 1
        self.next_id = nid
        return nid

    def find_service(self, service_name):
        '''
        返回对应服务名的服务器信息
        '''
        return ''

    def _test_call_method(self, method, kwargs):
        '''方便测试'''
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

    def _call_method(self, method, kwargs):
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
        server_info = self.find_service(method)
        if server_info:
            pass
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


class ChannelClient(ServerService):

    def __init__(self, keep_alive=False, on_server=False):
        '''
        :param keep_alive: 是否为长连接
        :param on_server: 是否是服务端发起的请求
        :return:
        '''
        ServerService.__init__(self)
        self.keep_alive = keep_alive
        self.stubs = {}  # 供长连接使用
        self.next_id = 0
        self.channel = None
        self.address = None
        self.on_server = on_server

    def get_request_id(self):
        nid = self.next_id
        if nid == MAX_REQUEST_ID:
            nid = 0
        nid += 1
        self.next_id = nid
        return nid

    def connect(self, address):
        '''
        异步connect
        '''
        self.address = address

    def real_connect(self):
        assert self.address, 'Not connected yet!'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.address)
        connection_class = net.tcp.KeepAliveConnection if self.keep_alive else net.tcp.Connection
        conn = connection_class(sock, None)
        self.channel = Channel(conn, self, ServerService_Stub)
        # init channel info on the other side
        info = ChannelInfo()
        info.on_server = self.on_server
        self.channel.stub.init_channel(None, info)

    def call_method(self, method_name, args):
        '''
        :param method_name: str
        :param args:  dict
        :return: block until something is returned
        '''
        if not self.channel:
            self.real_connect()
        req = CallRequest()
        req.request_id = self.get_request_id()
        req.method = method_name
        req.parameters = json.dumps(args)
        result = AsyncResult()
        self.replies[req.request_id] = result
        self.channel.stub.call_method(None, req)
        return result.get()

    def cast_method(self, method_name, args, callback=None):
        '''
        等同于异步call_method,需要callback
        '''
        def cast():
            ret = self.call_method(method_name, args)
            if callback:
                if isinstance(ret, list):
                    callback(*ret)
                else:
                    callback(ret)
        gevent.spawn(cast)


if __name__ == '__main__':
    client = ChannelClient(True)
    client.connect(('localhost', 63003))
    print client.call_method('1.B', {'test': 23})

