#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 16:40
# @Author  : Stan
# @File    : service.py

from net.rpc import rpc, Arg
from load_balance import ConsistentHash


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
            if hasattr(m, '_local_func'):
                self.service_names.append('.'.join([self.__class__.__name__, m.__name__]))

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


class CenterService(Service):
    '''
    服务注册，发现服务类
    '''

    def __init__(self, server, others):
        super(CenterService, self).__init__(server)
        self.services = {}
        self.picker = ConsistentHash(hash)
        self.others = others
        self.is_leader = False

    @rpc(Arg('service'), Arg('addr'), Arg('keep', False))
    def register_service(self, service_name, address, is_keep_alive):
        print service_name, address, is_keep_alive

    def unregister_service(self):
        pass

    # @rpc
    def find_service(self, service_name, con):
        pass

    def on_server_start(self):
        print 'server start up'


if __name__ == '__main__':
    a = CenterService(None)
    print a.service_names

