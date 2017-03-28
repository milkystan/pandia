#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : service.py

from net.rpc import rpc, Arg
from net.proto_python import server_pb2
import json
from load_balance import ConsistentHash


class Service(object):
    '''
    各种服务的基类
    '''

    def __init__(self, server):
        self.server = server
        self.service_names = []  # str: class_name.service_name
        self.init_rpc_methods()

    def init_rpc_methods(self):
        for m in self.__class__.__dict__.values():
            if hasattr(m, '_local_func'):
                self.service_names.append('.'.join([self.__class__.__name__, m.__name__]))

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

    def __init__(self, server):
        super(CenterService, self).__init__(server)
        self.services = {}
        self.picker = ConsistentHash(hash)

    @rpc(Arg('service'), Arg('addr'), Arg('keep', False))
    def register_service(self, service_name, address, is_keep_alive):
        print service_name, address, is_keep_alive

    def unregister_service(self):
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



    def send_heart_beat(self, rpc_controller, request, done):
        channel = rpc_controller.channel
        channel.stub.reply_heart_beat(None, server_pb2.Void())


    def reply_heart_beat(self, rpc_controller, request, done):
        channel = rpc_controller.channel
        channel.state = channel.ST_RECEIVED
        channel.retried = 0

    def dispatch(self, method, kwargs):
        '''实现根据method分发调用'''
        raise NotImplementedError


if __name__ == '__main__':
    a = CenterService(None)
    print a.service_names

