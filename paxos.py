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
ACCEPTED = 2


class Acceptor(object):
    def __init__(self):
        self.proposal_id = None
        self.accept_value = None
        self.accept_id = None
        self.acceptor_round = 0

    def reset_acceptor(self):
        self.proposal_id = None
        self.accept_value = None
        self.accept_id = None

    def on_pre_proposal(self, p_round, pid, pre_cb):
        if p_round > self.acceptor_round:
            self.reset_acceptor()
            self.acceptor_round = p_round
        aid = ava = None
        if self.proposal_id and pid > self.proposal_id or not self.proposal_id:
            self.proposal_id = pid
            aid, ava = self.accept_value, self.accept_value
        pre_cb and pre_cb(aid, ava)
        return aid, ava

    def on_proposal(self, p_round, pid, value, pro_cb):
        if p_round > self.acceptor_round:
            self.reset_acceptor()
            self.acceptor_round = p_round
        acc = False
        if self.proposal_id and pid >= self.proposal_id or not self.proposal_id:
            self.accept_value = value
            self.accept_id = pid
            acc = True
        pro_cb and pro_cb(acc)
        return acc


class Proposer(object):

    def __init__(self, pid, value, acceptors, learners):
        self.id = pid
        self.value = value
        self.acceptors = acceptors
        self.learners = learners
        self.pre_proposal_reply = None
        self.max_pre_proposal_reply_id = None
        self.pre_proposal_num = 0
        self.accepted_num = 0
        self.proposal_reply = 0
        self.state = PRE_PROPOSAL
        self.proposer_round = 0

    def reset_proposer(self):
        self.pre_proposal_reply = None
        self.max_pre_proposal_reply_id = None
        self.pre_proposal_num = 0
        self.accepted_num = 0
        self.proposal_reply = 0
        self.state = PRE_PROPOSAL

    def send_pre_proposal(self):
        for s in self.acceptors:
            s.on_pre_proposal(self.proposer_round, self.id, self.pre_proposal_cb)

    def send_proposal(self):
        for s in self.acceptors:
            s.on_proposal(self.proposer_round, self.id, self.value, self.proposal_cb)

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

    def proposal_cb(self, accepted):
        if self.state == PROPOSAL:
            if accepted:
                self.accepted_num += 1
                if self.accepted_num > len(self.acceptors) / 2:
                    self.state = ACCEPTED
                    self.notify_learner()

    def notify_learner(self):
        for l in self.learners:
            l.on_accept(self.id, self.value)


class Learner(object):
    def __init__(self):
        self.learned_pid = None
        self.learned_value = None

    def reset_learner(self):
        self.learned_pid = None
        self.learned_value = None

    def on_accept(self, pid, value):
        self.learned_pid = pid
        self.learned_value = value
        print pid, value, 'choosed'
        return pid, value


if __name__ == '__main__':
    a1 = Acceptor()
    a2 = Acceptor()
    a3 = Acceptor()
    aa = [a1, a2, a3]
    l = [Learner()]
    p1 = Proposer(1, 'p1', aa, l)
    p2 = Proposer(2, 'p2', aa, l)
    p1.send_pre_proposal()
    p2.send_pre_proposal()