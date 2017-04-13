#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/10 18:51
# @Author  : Stan
# @File    : paxos.py

'''
实现paxos算法
'''

from collections import defaultdict

PRE_PROPOSAL = 0
PROPOSAL = 1
SELECTED = 2


class Acceptor(object):
    def __init__(self, learners):
        self.learners = learners
        self.proposal_id = None
        self.accept_value = None


    def notify_learner(self, pid, value):
        for l in self.learners:
            l.on_accept(pid, value)


    def on_pre_proposal(self, pid, value, cb):
        if self.proposal_id and pid > self.proposal_id or not self.proposal_id:
            self.proposal_id = pid
            cb()
        else

    def on_proposal(self, pid, value):
        if self.proposal_id and pid > self.proposal_id or not self.proposal_id:
            self.accept_value = value
            self.notify_learner(pid, value)



class Proposer(object):

    def __init__(self, pid, value, acceptors):
        self.id = pid
        self.value = value
        self.acceptors = acceptors
        self.pre_proposal_reply = None
        self.max_pre_proposal_reply_id = None
        self.pre_proposal_num = 0
        self.proposal_reply = 0
        self.state = PRE_PROPOSAL

    def send_pre_proposal(self):
        for s in self.acceptors:
            s.on_pre_proposal(self.id, self.value, self.pre_proposal_cb)

    def send_proposal(self):
        for s in self.acceptors:
            s.on_proposal(self.id, self.value)

    def pre_proposal_cb(self, rid, reply):
        if self.state == PRE_PROPOSAL:
            self.pre_proposal_num += 1
            if rid:
                if self.max_pre_proposal_reply_id and rid > self.max_pre_proposal_reply_id:
                    self.max_pre_proposal_reply_id = rid
                    self.pre_proposal_reply = reply
                elif not self.max_pre_proposal_reply_id:
                    self.max_pre_proposal_reply_id = rid
                    self.pre_proposal_reply = reply
            if self.pre_proposal_num > len(self.acceptors) / 2:
                self.state = PROPOSAL
                if self.pre_proposal_reply:
                    self.value = self.pre_proposal_reply
                self.send_proposal()



class Leaner(object):
    def __init__(self, acceptor_num):
        self.acceptor_num = acceptor_num
        self.proposals = defaultdict(int)
        self.value = None
        self.state = PROPOSAL

    def on_accept(self, pid, value):
        if self.state == PROPOSAL:
            self.proposals[pid] += 1
            if self.proposals[pid] > self.acceptor_num / 2:
                self.value = value
            self.state = SELECTED

