#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 19:51
# @Author  : Stan
# @File    : tcp.py

import gevent
from gevent import socket


class TcpConnection(object):
    def __init__(self, socket, peer):
        self.socket = socket
        self.peer = peer
        self.handler = None

    def set_handler(self, handler):
        self.handler = handler

    def send(self, data):
        pass

    def recv(self, size):
        pass




class TcpClient(TcpConnection):
    pass


class TcpServer(object):
    pass


def foo1():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 63333))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        print 1,2


def foo2():
    import time
    while True:
        time.sleep(3)
        print '222'

def foo3():
    import time

    print 2

if __name__ == '__main__':
    f1 = gevent.spawn(foo3)
    f1.join()
    gevent.sleep(0)
    import greenlet
    greenlet.greenlet
