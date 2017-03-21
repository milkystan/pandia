#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 15:31
# @Author  : Stan
# @File    : client.py

import gevent


class Client(object):
    def __init__(self):
        pass

    def call(self, method, kwargs, callback=None):
        '''
        阻塞调用call
        :param method: 方法名
        :param kwargs: 参数字典
        :param callback: 不需要设置
        :return: 远程rpc的返回值
        '''
        pass

    def cast(self, method, kwargs, callback=None):
        '''
        阻塞调用cast
        :param method: 方法名
        :param kwargs: 参数字典
        :param callback: 不需要设置
        :return: None
        '''
        pass

    def async_call(self, method, kwargs, callback=None):
        '''
        异步调用call
        :param method: 方法名
        :param kwargs: 参数字典
        :param callback: 回调函数
        :return: Greenlet对象
        '''
        return gevent.spawn(self.call, method, kwargs, callback=callback)

    def async_cast(self, method, kwargs, callback=None):
        '''
        异步调用cast
        :param method: 方法名
        :param kwargs: 参数字典
        :param callback: 回调函数
        :return: Greenlet对象
        '''
        return gevent.spawn(self.cast, method, kwargs, callback=callback)


if __name__ == '__main__':
    pass