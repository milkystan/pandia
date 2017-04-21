#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 21:18
# @Author  : Stan
# @File    : test.py.py


import socket
import gevent
import time
from gevent import socket
import tcp


class F(object):

    def __init__(self, a):
        pass

    def handle_data(self, data):
        print data


def foo(sok):
    print 11
    sok.send('gggggg')


def server():
    s = socket.socket()
    s.bind(('0.0.0.0', 63000))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        tcp.KeepAliveConnection(cli, addr, F)


def connect():
    import socket as o_socket
    s = o_socket.socket()
    s.connect(('localhost', 9900))

if __name__ == '__main__':
    connect()