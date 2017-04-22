#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/21 21:14
# @Author  : Stan
# @File    : start_center.py
'''
一：中心服务节点：分为永久节点，临时节点
    1. 永久节点：配置在config中
    2. 临时节点：无需配置，临时启动服务节点

二：扩容方法：
    1. 通过临时节点（关闭集群后，临时节点信息丢失）[临时方案]
    2. 配置config，设置永久节点，启动新节点，并依次重启旧节点，也会丢失临时节点

三：必须保证半数以上的永久节点可用，否则无法启动集群
'''
