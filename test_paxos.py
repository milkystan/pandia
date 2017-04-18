#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/18 15:52
# @Author  : Stan
# @File    : test_paxos.py

from paxos import *
import threading
import time
import random


def test(p_n, a_n):
    def ramdom_start(p, t):
        time.sleep(t)
        p.send_pre_proposal()

    acceptors = []
    for i in range(a_n):
        acceptors.append(Acceptor())
    learners = [Learner()]
    for i in range(p_n):
        p = Proposer(i, 'p' + str(i), acceptors, learners)
        t = threading.Thread(target=ramdom_start, args=(p, random.random() * 3))
        t.start()


if __name__ == '__main__':
    test(20, 6)