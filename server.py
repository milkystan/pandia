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
        self._wait_time = None
        self._max_retries = None
        self.keep_alive_loop = None

    def add_service(self, service_class):
        self.services[service.__name__] = service_class(self)

    def dispatch(self, rpc_method, kwargs):
        '''
        派发请求至对应的Service
        '''
        service, m_name = rpc_method.split('.')
        return {'test': 'test121334'}


    def stop(self):
        self._stop = True


    def set_keep_alive(self, wait_time, max_retries):
        '''服务端发送心跳包'''
        self._wait_time = wait_time
        self._max_retries = max_retries
        if not self.keep_alive_loop:
            self.keep_alive_loop = gevent.spawn(self._send_heart_beat)


    def _send_heart_beat(self):
        while not self._stop:
            gevent.sleep(self._wait_time)
            for i in self.channels.keys():
                if i in self.channels: # 因为协程可能在调用send_heat_beat的时候切出去，切回后需要检查
                    channel = self.channels[i]
                    if channel.state == channel.ST_WAIT:
                        if channel.retried > self._max_retries:
                            self.handle_keep_alive_failed(i)
                            continue
                        else:
                            channel.retried += 1
                    channel.state = channel.ST_WAIT
                    channel.stub.send_heart_beat(None, server_pb2.Void())



    def handle_keep_alive_failed(self, key):
        del self.channels[key]
        print key, 'failed in keep alive'


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
    server.set_keep_alive(2, 3)
    server.run()
