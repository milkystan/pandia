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

# config
{
    'name': {
        'address": ('0.0.0.0', 33333),
        'keep_alive': True # 表示使用长连接
    }

}