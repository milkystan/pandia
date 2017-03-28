#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/28 15:04
# @Author  : Stan
# @File    : load_balance.py
'''
Hash algorithm for load balance
'''

import math


class SimpleHash(object):
    def __init__(self, hash_func):
        self.hash_func = hash_func

    def pick(self, obj, candidate_list):
        '''
        :param obj: a object can be hashed by self.hash_func
        :param candidate_list: a list contains all the candidates
        :return:
        '''
        n = len(candidate_list)
        return candidate_list[self.hash_func(obj) % n]


class ConsistentHash(SimpleHash):
    def __init__(self, hash_func, min_node=8, ring_length=2**16):
        '''
        :param hash_func:
        :param min_node: If the num of candidates is less than this value,
        virtual nodes will be added.
        :param ring_length: the length of the ring
        :return:
        '''
        super(ConsistentHash, self).__init__(hash_func)
        self.min_node = min_node
        self.ring = ring_length

    def pick(self, obj, candidate_list):
        n = len(candidate_list)
        c_list = candidate_list
        candidate_hash = {}
        ring = self.ring
        h_f = self.hash_func
        if n < self.min_node:
            x = int(math.ceil(self.min_node / float(n)))
            c_list = [(i, j) for i in candidate_list for j in range(x)]
            for i in c_list:
                candidate_hash[h_f(i) % ring] = i[0]
        else:
            for i in c_list:
                candidate_hash[h_f(i) % ring] = i

        obj_hash = h_f(obj) % ring
        array = candidate_hash.keys()
        array.sort()
        for k in array:
            if obj_hash <= k:
                key = k
                break
        else:
            key = array[0]
        return candidate_hash[key]


if __name__ == '__main__':
    a = ConsistentHash(hash)
    print a.pick(3, [1,2,3,4])