#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
tornado_server.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2014-02-26
'''
import tornado.websocket
import tornado.ioloop
import tornado.autoreload
import tornado.httpserver
import tornado.web
import redis
import threading
from functools import partial
import os
import socket
import sqlite3
import time
import json


PORT = 9999

red = redis.StrictRedis()
LISTENERS = []


def redis_listener():
    ps = red.pubsub()
    ps.subscribe('chat')
    io_loop = tornado.ioloop.IOLoop.instance()
    for message in ps.listen():
        for element in LISTENERS:
            io_loop.add_callback(partial(element.on_message, message))

def the_eye_tribe_deformat(data):
    x = data['values']['frame']['avg']['x']
    y = data['values']['frame']['avg']['y']
    left_x = data['values']['frame']['lefteye']['avg']['x']
    left_y = data['values']['frame']['lefteye']['avg']['y']
    right_x = data['values']['frame']['righteye']['avg']['x']
    right_y = data['values']['frame']['righteye']['avg']['y']
    return dict(
                x = x,
                y = y,
                left = dict(
                            x = left_x,
                            y = left_y,
                            ),
                right = dict(
                            x = right_x,
                            y = right_y
                            ),
                )


class RealTimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        LISTENERS.append(self)

    def on_message(self, messgae):
        data = json.loads(messgae['data'])
        result = the_eye_tribe_deformat(data)
        self.write_message(json.dumps(result))

    def on_close(self):
        LISTENERS.remove(self)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class DemoHandler(tornado.web.RequestHandler):
    def get(self, template_name):
        return self.render('%s.html'%template_name)

settings = {
        'auto_reload': True,
        'template_path': os.path.join(os.path.dirname(__file__), "templates"),
        'static_path': os.path.join(os.path.dirname(__file__), "static"),
        'Debug': True,
         }

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/realtime/", RealTimeHandler),
    (r"/demo/(\w+)", DemoHandler),
], **settings)


if __name__ == '__main__':
    t = threading.Thread(target=redis_listener)
    t.daemon = True
    t.start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    try:
        print 'running on http://127.0.0.1:%s'%PORT
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
