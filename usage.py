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
        'address': '192.168.0.12: 67804'
        'keep_alive': True # 表示使用长连接, client从center中获得是否使用长连接，需要保活(心跳包)
    }

}