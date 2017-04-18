#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : service.py

from net.rpc import rpc, Arg


class Service(object):
    '''
    各种服务的基类
    子类需要实现on_server_start方法
    '''

    def __init__(self, server):
        self.server = server
        self.service_names = []  # str: class_name.service_name
        self.init_rpc_methods()

    def init_rpc_methods(self):
        for m in self.__class__.__dict__.values():
            if hasattr(m, 'local_func'):
                self.service_names.append(m.__name__)

    # @rpc
    def stop_server(self, con):
        '''
        关闭服务器
        '''
        self.server.stop()


    def on_server_start(self):
        '''
        服务器启动时会调用各个service对象的该方法
        '''
        raise NotImplementedError






if __name__ == '__main__':
    a = CenterService(None)
    print a.service_names

