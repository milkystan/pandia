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
        self.rev_loop = gevent.spawn(self._receive_loop)



    def __call__(self, handler):
        '''easy way to set handler'''
        self.handler = handler
        return self


    def send(self, data):
        length = len(data)
        assert length < MAX_LEN, 'Too much data to send!'
        s_data = struct.pack('<I', length) + data
        try:
            self.socket.sendall(s_data)
        except Exception, e:
            print e, __file__
            self.handler.handle_socket_error()

    def _receive_loop(self):
        '''处理半包'''
        sock = self.socket
        r_data = ''
        state = PACK_ST
        data_len = None
        while not self._stop:
            try:
                r_data += sock.recv(4096)
            except Exception, e:
                print e, __file__
                self.handler.handle_socket_error()
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


class AdvancedConnection(object):
    '''
    可以在长连接和短连接中切换
    需要传入gevent.socket的socket对象
    '''

    def __init__(self, sock, peer, keep_alive=False):
        self.socket = sock
        self.peer = peer
        self.handler = None
        self._stop = False
        self.keep_alive = keep_alive
        self.rev_loop = gevent.spawn(self._receive_loop)

    def __call__(self, handler):
        '''easy way to set handler'''
        self.handler = handler
        return self

    def send(self, data):
        length = len(data)
        assert length < MAX_LEN, 'Too much data to send!'
        s_data = struct.pack('<I', length) + data
        try:
            self.socket.sendall(s_data)
        except Exception, e:
            print e, __file__
            self.handler.handle_socket_error()

    def close(self):
        self._stop = True
        self.socket.close()

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
                print e, __file__
            length = len(r_data)
            if state == PACK_ST:
                if length >= INT_SIZE:
                    data_len = struct.unpack('<I', r_data[:INT_SIZE])[0]
                    state = PACK_MI

            if state == PACK_MI and length >= data_len + INT_SIZE:
                # 如果是默认的短连接，则阻塞运行第一次任务，等待其完成后确定是否需要保持该连接
                # 当确定为长连接后，异步调用之后的任务
                if not self.keep_alive:
                    self.handler.handle_data(r_data[INT_SIZE: INT_SIZE + data_len])
                    # 首次任务后确定为短连接，则退出循环，关闭socket
                    if not self.keep_alive:
                        self.close()
                else:
                    gevent.spawn(self.handler.handle_data, r_data[INT_SIZE: INT_SIZE + data_len])
                    r_data = r_data[INT_SIZE + data_len:]
                    state = PACK_ST



