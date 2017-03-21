#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 20:18
# @Author  : Stan
# @File    : channel.py

from google.protobuf.service import RpcChannel, RpcController


class Channel(RpcChannel):
    def __init__(self, service, connection):
        super(RpcChannel, self).__init__()
        self.service = service
        self.connection = connection

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        self.connection.send()


class Controller(RpcController):
    '''
    持有Channel对象的引用，供返回调用
    '''
    def __init__(self, channel):
        super(Controller, self).__init__()
        self.channel = channel

