#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/18 21:18
# @Author  : Stan
# @File    : test_center.py

import server
import center_service
from threading import Thread
centers = [('localhost', 8785), ('localhost', 8786), ('localhost', 8787)]

def run_server(i, addr):
    s = server.Server(addr)
    service = center_service.CenterService(s, i, centers)
    s.add_service(service)
    s.set_keep_alive(2, 3)
    s.run()

def run_centers():
    for i, c in enumerate(centers):
        t = Thread(target=run_server, args=(i, c))
        t.start()

if __name__ == '__main__':
    run_centers()