#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/21 21:21
# @Author  : Stan
# @File    : test2.py

import socket

s = socket.socket()
s.connect(('localhost', 63000))
s.send('hhhh')

while True:
    print s.recv(4096)