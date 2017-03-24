#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 19:51
# @Author  : Stan
# @File    : tcp.py

import gevent
import struct

INT_SIZE = 4
SHORT_SIZE = 2
MAX_LEN = 2 ** (INT_SIZE * 8) - 1
PACK_ST = 0
PACK_MI = 1


class Connection(object):
    '''
    短连接，需要传入gevent.socket的socket对象
    '''
    def __init__(self, sock, peer):
        self.socket = sock
        self.peer = peer
        self.handler = None
        self._stop = False
        gevent.spawn(self._receive_loop)


    def set_handler(self, handler):
        self.handler = handler


    def send(self, data):
        length = len(data)
        assert length < MAX_LEN, 'Too much data to send!'
        s_data = struct.pack('<I', length) + data
        self.socket.sendall(s_data)

    def _receive_loop(self):
        '''处理半包'''
        sock = self.socket
        r_data = ''
        state = PACK_ST
        data_len = None
        while not self._stop:
            print 'in'
            try:
                r_data += sock.recv(4096)
            except Exception, e:
                print e
            length = len(r_data)
            if state == PACK_ST:
                if length >= INT_SIZE:
                    data_len = struct.unpack('<I', r_data[:INT_SIZE])[0]
                    state = PACK_MI
            if state == PACK_MI and length >= data_len + INT_SIZE:
                return self.handler.handle_data(r_data[INT_SIZE: INT_SIZE + data_len])

    def close(self):
        self._stop = True
        self.socket.close()


class KeepAliveConnection(Connection):
    '''
    长连接
    '''
    def _receive_loop(self):
        '''处理粘包，半包问题'''
        sock = self.socket
        r_data = ''
        state = PACK_ST
        data_len = None
        while not self._stop:
            try:
                r_data += sock.recv(4096)
            except Exception, e:
                print e
            length = len(r_data)
            if state == PACK_ST:
                if length >= INT_SIZE:
                    data_len = struct.unpack('<I', r_data[:INT_SIZE])[0]
                    state = PACK_MI

            if state == PACK_MI and length >= data_len + INT_SIZE:
                gevent.spawn(self.handler.handle_data, r_data[INT_SIZE: INT_SIZE + data_len])
                r_data = r_data[INT_SIZE + data_len:]
                state = PACK_ST



