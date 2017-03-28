#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 19:51
# @Author  : Stan
# @File    : rpc.py

import functools


class Arg(object):
    '''
    rpc参数类型
    '''
    def __init__(self, key, default=None):
        '''
        key : rpc传输时的key值
        default : 未传输该key时的默认值
        '''
        self.key = key
        self.default = default


def rpc(*rpc_args):
    def outer(func):

        @functools.wraps(func)
        def inner(self, p_dict):
            params = [self]
            for a in rpc_args:
                assert isinstance(a, Arg), 'The type of arguments in rpc decorator must be Arg!'
                params.append(p_dict.get(a.key) or a.default)
            return func(*params)
        inner._local_func = func
        return inner
    return outer
