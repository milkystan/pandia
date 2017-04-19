#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/30 15:48
# @Author  : Stan
# @File    : rpc_service.py

from net.proto_python import server_pb2
import json


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

    def init_channel(self, rpc_controller, request, done):
        channel = rpc_controller.channel
        channel.peer_on_server = request.on_server

    def dispatch(self, method, kwargs):
        '''实现根据method分发调用'''
        raise NotImplementedError
