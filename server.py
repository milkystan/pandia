#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : server.py

import gevent
from gevent import socket
from service import _ServerService
import bson


class Server(object):
    '''
    承载Service的服务器
    '''
    def __init__(self, address):
        self.address = address
        self.services = []
        self._stop = False
        self.server_service = _ServerService(self)

    def add_service(self, service):
        if service not in self.services:
            self.services.append(service)

    def dispatch(self, con, peer):
        '''
        派发请求至对应的Service
        '''
        pass

    def stop(self):
        self._stop = True

    def run(self):
        b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        b_socket.bind(self.address)
        b_socket.listen(65535)
        while not self._stop:
            con, peer = b_socket.accept()
            gevent.spawn(self.dispatch, con, peer)


if __name__ == '__main__':
    server = Server(('0.0.0.0', 63333))
    server.run()
