#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/22 16:03
# @Author  : Stan
# @File    : dispatcher.py

'''
A dispatcher based on gevent
'''

from gevent import socket

socket_map = {}


class Dispatcher(object):
    def __init__(self):
        pass

    def handle_expt(self):
        pass

    def handle_read(self):
        pass

    def handle_write(self):
        pass

    def handle_connect(self):
        pass

    def handle_accept(self):
        pass

    def handle_close(self):
        pass


