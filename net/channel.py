#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 20:18
# @Author  : Stan
# @File    : channel.py

from google.protobuf.service import RpcChannel, RpcController
import struct
from net.tcp import SHORT_SIZE
import gevent


class Channel(RpcChannel):
    def __init__(self, conn, service, stub_class):
        super(RpcChannel, self).__init__()
        self.service = service
        self.stub = stub_class(self)
        self.conn = conn(self)
        self.ctrl = Controller(self)

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        index = method_descriptor.index
        data = struct.pack('<H', index) + request.SerializeToString()
        self.conn.send(data)

    def handle_data(self, data):
        try:
            method_index = struct.unpack('<H', data[:SHORT_SIZE])[0]
            method = self.service.GetDescriptor().methods[method_index]
            request = self.service.GetRequestClass(method)()
            request.ParseFromString(data[SHORT_SIZE:])
            response = self.service.CallMethod(method, self.ctrl, request, None)
            if response:
                self.stub.send_response(None, response)

        except Exception, e:
            raise


    def handle_close(self):
        pass


class Controller(RpcController):
    '''
    持有Channel对象的引用，供返回调用
    '''
    def __init__(self, channel):
        super(Controller, self).__init__()
        self.channel = channel

