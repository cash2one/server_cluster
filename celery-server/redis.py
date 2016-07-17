#!/usr/bin/env python
# encoding: utf-8
"""
@author: yanjianlong
@contact: yanjianlong@126.com
@time: 7/15/2016 2:40 PM
"""
import redis
ip = "10.25.104.65"
port = 6381
r = redis.StrictRedis(host=ip, port=port, db=0)

def rpush(cmd):
    name = "special_channel_mt4"
    name = "test"
    r.set(name, cmd)
    r.rpush(name, cmd)