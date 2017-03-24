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
    def __init__(self, server):
        server_pb2.ServerService.__init__(self)
        self.server = server

    def call_method(self, rpc_controller, request, done):
        method_name = request.method
        kwargs = json.loads(request.parameters)
        qid = request.request_id
        ret = self.server.dispatch(method_name, kwargs)
        stub = server_pb2.ServerService_Stub(rpc_controller.channel)
        response = server_pb2.CallResponse()
        response.response_id = qid
        response.success = True
        response.content = json.dumps(ret)
        print 'before send'
        stub.send_response(None, response)
        print 'send'

    def send_response(self, rpc_controller, request, done):
        print request.SerializeToString()
        print 'inin'





