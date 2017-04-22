#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/18 16:54
# @Author  : Stan
# @File    : center_service.py

import service
import paxos
from load_balance import ConsistentHash
from net.rpc import rpc, Arg
from client import ChannelClient


class AcceptorProxy(paxos.Acceptor):
    def __init__(self, client, is_remote):
        '''
        :param client:
        :param is_remote: bool，表示client是否为远端对象
        :return:
        '''
        super(AcceptorProxy, self).__init__()
        self.client = client
        self.is_remote = is_remote

    def on_pre_proposal(self, p_round, pid, pre_cb):
        if self.is_remote:
            self.client.cast_method('CenterService.on_pre_proposal', {'pr': p_round, 'pid': pid}, pre_cb)
        else:
            self.client.on_pre_proposal.local_func(self.client, p_round, pid, pre_cb)

    def on_proposal(self, p_round, pid, value, pro_cb):
        if self.is_remote:
            self.client.cast_method('CenterService.on_proposal', {'pr': p_round, 'pid': pid, 'value': value}, pro_cb)
        else:
            self.client.on_proposal.local_func(self.client, p_round, pid, value, pro_cb)


class LearnerProxy(paxos.Learner):
    def __init__(self, client, is_remote):
        '''
        :param client:
        :param is_remote: bool，表示client是否为远端对象
        :return:
        '''
        super(LearnerProxy, self).__init__()
        self.client = client
        self.is_remote = is_remote

    def on_accept(self, pid, value):
        if self.is_remote:
            self.client.cast_method('CenterService.on_accept', {'pid': pid, 'value': value})
        else:
            self.client.on_accept.local_func(self.client, pid, value)


class CenterService(service.Service, paxos.Acceptor, paxos.Proposer, paxos.Learner):
    '''
    实现基于Paxos算法的leader选举服务
    提供服务注册，发现服务
    '''

    def __init__(self, server, sid, centers):
        service.Service.__init__(self, server)
        paxos.Acceptor.__init__(self)
        paxos.Learner.__init__(self)
        acceptors = []
        learners = []
        for index, address in enumerate(centers):
            if index == sid:
                c, f = self, False
            else:
                c, f = ChannelClient(True), True
                c.connect(address)  # 异步connect，不会阻塞
            acceptors.append(AcceptorProxy(c, f))
            learners.append(LearnerProxy(c, f))
        paxos.Proposer.__init__(self, sid, sid, acceptors, learners)
        self.services = {}
        self.picker = ConsistentHash(hash)
        self.centers = centers
        self.is_leader = False

    def on_server_start(self):
        '''
        开始leader选举
        '''
        self.send_pre_proposal()

    def on_del_channel(self, channel):
        '''
        重新选举
        '''
        self.proposer_round += 1
        self.reset_proposer()
        self.reset_learner()
        self.send_pre_proposal()

    def on_add_channel(self, channel):
        pass

    # Acceptor
    @rpc(Arg('pr'), Arg('pid'), Arg('pre_cb', None))
    def on_pre_proposal(self, p_round, pid, pre_cb):
        return super(CenterService, self).on_pre_proposal(p_round, pid, pre_cb)

    @rpc(Arg('pr'), Arg('pid'), Arg('value'), Arg('pro_cb', None))
    def on_proposal(self, p_round, pid, value, pro_cb):
        return super(CenterService, self).on_proposal(p_round, pid, value, pro_cb)

    # Learner
    @rpc(Arg('pid'), Arg('value'))
    def on_accept(self, pid, value):
        return super(CenterService, self).on_accept(pid, value)

    # 服务注册服务
    @rpc(Arg('service'), Arg('addr'), Arg('keep', False))
    def register_service(self, service_name, address, is_keep_alive):
        print service_name, address, is_keep_alive

    def unregister_service(self):
        pass

    # @rpc
    def find_service(self, service_name, con):
        pass


if __name__ == '__main__':
    pass
