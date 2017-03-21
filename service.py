#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : service.py

from net.rpc import rpc


class Service(object):
    '''
    各种服务的基类
    '''
    def __init__(self, server):
        self.server = server

    @rpc('xx')
    def stop_server(self, con):
        '''
        关闭服务器
        '''
        self.server.stop()


class CenterService(Service):
    '''
    服务注册，发现服务类
    '''

    @rpc
    def register_service(self, con):
        pass


    @rpc
    def find_service(self, service_name, con):
        pass


class _ServerService(object):
    '''
    提供Server基本的服务，例如call_method等
    '''
    def __init__(self, server):
        self.server = server


