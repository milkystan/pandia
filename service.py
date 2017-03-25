#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : service.py

from net.rpc import rpc
from net.proto_python import server_pb2
import json


class Service(object):
    '''
    各种服务的基类
    '''
    def __init__(self, server):
        self.server = server

    # @rpc
    def stop_server(self, con):
        '''
        关闭服务器
        '''
        self.server.stop()


class CenterService(Service):
    '''
    服务注册，发现服务类
    '''

    # @rpc
    def register_service(self, con):
        pass


    # @rpc
    def find_service(self, service_name, con):
        pass


class ServerService(server_pb2.ServerService):
    '''
    提供Server基本的服务，例如call_method等
    '''
    def __init__(self):
        server_pb2.ServerService.__init__(self)
        self.replies = {}

    def call_method(self, rpc_controller, request, done):
        '''解析请求，派发至对应的sub service'''
        method_name = request.method
        kwargs = json.loads(request.parameters)
        ret = self.dispatch(method_name, kwargs)
        response = server_pb2.CallResponse()
        response.response_id = request.request_id
        response.content = json.dumps(ret)
        return response


    def send_response(self, rpc_controller, request, done):
        '''接收返回值'''
        rid = request.response_id
        if rid in self.replies:
            self.replies[rid].set(json.loads(request.content))


    def dispatch(self, method, kwargs):
        '''实现根据method分发调用'''
        raise NotImplementedError





