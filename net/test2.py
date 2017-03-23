#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/21 21:21
# @Author  : Stan
# @File    : test2.py

import socket
import tcp
import test
import time
s = socket.socket()
s.connect(('localhost', 63000))
con = tcp.Connection(s, None, test.F)
s = '1' * 67
while True:
    time.sleep(0.01)
    con.send(s)

