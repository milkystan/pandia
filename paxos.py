#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 18:51
# @Author  : Stan
# @File    : paxos.py

'''
实现paxos算法
'''


class Acceptor(object):
    def __init__(self):
        pass

    def on_pre_proposal(self):
        pass

    def on_proposal(self):
        pass


class Proposer(object):
    def __init__(self, value, acceptors):
        self.value = value
        self.acceptors = acceptors

    def pre_proposal(self):
        pass

    def proposal(self):
        pass


class Leaner(object):
    pass

