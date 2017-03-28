#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/28 19:27
# @Author  : Stan
# @File    : config.py

from service import CenterService

SERVICE_CENTER = 0
ADDRESS = 1
KEEP_ALIVE = 2
SERVICES = 3

CONF = {
    'center1': {
        SERVICE_CENTER: True,
        ADDRESS: '127.0.0.1:63200',
        KEEP_ALIVE: True,
        SERVICES: [CenterService]

    },
    'server1': {
        SERVICE_CENTER: False,
        ADDRESS: '127.0.0.1:65555',
        KEEP_ALIVE: False,
        SERVICES: []
    }
}