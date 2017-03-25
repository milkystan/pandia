#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : server.py

import gevent
from gevent import socket
import net.tcp
from net.channel import *
from net.proto_python import server_pb2
import json
import service


class Server(service.ServerService):
    '''
    承载Service的服务器
    '''
    def __init__(self, address):
        service.ServerService.__init__(self)
        self.address = address
        self._stop = False
        self.channels = {}  # 保存connection引用

    def add_service(self, service):
        self.services[service.__name__] = service

    def dispatch(self, rpc_method, kwargs):
        '''
        派发请求至对应的Service
        '''
        service, m_name = rpc_method.split('.')
        return {'test': 'test121334'}

    def stop(self):
        self._stop = True

    def run(self):
        b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        b_socket.bind(self.address)
        b_socket.listen(65535)
        while not self._stop:
            sock, peer = b_socket.accept()
            conn = net.tcp.Connection(sock, peer)
            channel = Channel(conn, self, server_pb2.ServerService_Stub)
            self.channels['t'] = channel


if __name__ == '__main__':
    server = Server(('0.0.0.0', 63003))
    server.run()
