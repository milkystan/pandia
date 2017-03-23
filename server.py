#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : server.py

import gevent
from gevent import socket
from service import ServerService
import net.tcp
from net.channel import *
import bson


class Server(object):
    '''
    承载Service的服务器
    '''
    def __init__(self, address):
        self.address = address
        self.services = []
        self._stop = False
        self.server_service = ServerService(self)
        self.conns = {}  # 保存connection引用

    def add_service(self, service):
        if service not in self.services:
            self.services.append(service)

    def dispatch(self, sock, peer):
        '''
        派发请求至对应的Service
        '''
        conn = net.tcp.Connection(sock, peer)
        channel = Channel(self.server_service, conn)
        self.conns['t'] = channel

    def stop(self):
        self._stop = True

    def run(self):
        b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        b_socket.bind(self.address)
        b_socket.listen(65535)
        while not self._stop:
            sock, peer = b_socket.accept()
            gevent.spawn(self.dispatch, sock, peer)


if __name__ == '__main__':
    server = Server(('0.0.0.0', 63000))
    server.run()
