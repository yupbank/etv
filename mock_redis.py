#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mock_redis.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-02-28
'''
import redis
import time
import random


def main():
    red = redis.StrictRedis()
    ps = red.pubsub()
    ps.subscribe('chat')
    while True:
        time.sleep(1)
        red.publish('chat', '{"category":"tracker","request":"get","statuscode":200,"values":{"frame":{"avg":{"x":%s,"y":%s},"fix":false,"lefteye":{"avg":{"x":%s,"y":%s},"pcenter":{"x":0.3302603960037231,"y":0.3749265968799591},"psize":26.01136016845703,"raw":{"x":0.0,"y":0.0}},"raw":{"x":0.0,"y":0.0},"righteye":{"avg":{"x":%s,"y":%s},"pcenter":{"x":0.4942050576210022,"y":0.3712331652641296},"psize":26.94578170776367,"raw":{"x":0.0,"y":0.0}},"state":6,"time":219168}}}'%(random.randrange(0, 1400), random.randrange(0, 960),random.randrange(0, 1400), random.randrange(0, 960),random.randrange(0, 1400), random.randrange(0, 960)))
        print 'sending...'

if __name__ == '__main__':
    main()
