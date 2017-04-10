#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 11:19
# @Author  : Stan
# @File    : usage.py

import server
# server = Server([service1])
# server.run()
#
# client = Client('center address')
# client.call('A.b', 1, 2)
# client.cast('A.b', 3)
# client.async_call('A.b', 1, cb)
# client.async_cast('A.b', 1, cb)

# config
SERVER_CONF = {
    'center': {
        'center1': {
            'ip': '127.0.0.0',
            'port': 78787,
            'local_start': True,
        },
        'center2': {
            'ip': '127.0.0.0',
            'port': 78785,
            'local_start': True
        }
    },
    'server': {
        'server1': {
            'ip': '',
            'port': 89897,
            'services': [],
            'keep_alive': True
        },
        'server2': {

        }
    }

}