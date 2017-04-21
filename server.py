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
import rpc_service


class Server(rpc_service.ServerService):
    '''
    承载Service的服务器
    '''
    def __init__(self, address):
        rpc_service.ServerService.__init__(self)
        self.address = address
        self._stop = False
        self.channels = {}  # 保存connection引用
        self._wait_time = None
        self._max_retries = None
        self.keep_alive_loop = None
        self.services = {}

    def add_service(self, service):
        self.services[service.__class__.__name__] = service

    def add_channel(self, channel):
        self.channels[channel.conn.peer] = channel

    def dispatch(self, rpc_method, kwargs):
        '''
        派发请求至对应的Service
        '''
        class_name, method_name = rpc_method.split('.')
        if class_name in self.services:
            s = self.services[class_name]
            if method_name in s.service_names:
                return getattr(s, method_name)(kwargs)
        return None

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
                if i in self.channels:  # 因为协程可能在调用send_heat_beat的时候切出去，切回后需要检查
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
        for s in self.services.values():
            s.on_lost_channel(self.channels[key])
        del self.channels[key]
        print key, 'failed in keep alive'

    def on_server_start(self):
        for s in self.services.values():
            s.on_server_start()

    def run(self):
        b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        b_socket.bind(self.address)
        b_socket.listen(65535)
        self.on_server_start()
        while not self._stop:
            sock, peer = b_socket.accept()
            conn = net.tcp.AdvancedConnection(sock, peer)  # 默认为短连接，根据需求转化为长连接
            channel = Channel(conn, self, server_pb2.ServerService_Stub)
            self.channels[conn.peer] = channel


if __name__ == '__main__':
    server = Server(('0.0.0.0', 63003))
    server.add_service()
    server.set_keep_alive(2, 3)
    server.run()
