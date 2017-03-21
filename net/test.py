#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 21:18
# @Author  : Stan
# @File    : test.py.py


import socket
import gevent
import time
from gevent import socket


def foo(sok):
    print 11
    sok.send('gggggg')


def server():
    s = socket.socket()
    s.bind(('0.0.0.0', 63000))
    s.listen(0)
    while True:
        cli, _ = s.accept()
        while True:
            print 1111
            gevent.sleep(0.2)
            gevent.spawn(foo, cli)



server()