#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 11:19
# @Author  : Stan
# @File    : usage.py

import server
server = Server([service1])
server.run()

client = Client('center address')
client.call('A.b', 1, 2)
client.cast('A.b', 3)
client.async_call('A.b', 1, cb)
client.async_cast('A.b', 1, cb)
