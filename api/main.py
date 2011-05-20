#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

import me
import stream
import round_
import user
import admin

import mongoengine
import tornado.web
import tornado.ioloop


def main():
    #mongoengine.connect('blafio')
    mongoengine.connect('blafio-dev', 
        host='flame.mongohq.com', 
        port=27100, 
        username='exavolt', 
        password='000000'
        )
    handlers = [
        (r"/1.0/home/stream/([A-Za-z0-9_]+).json", me.HomeStreamHandler),
        (r"/1.0/me/stream/([A-Za-z0-9_]+).json", me.SelfStreamHandler),
        (r"/1.0/stream.json", stream.Handler),
        (r"/1.0/round/(start|finish|reset|interrupt|resume).json", round_.Handler),
        (r"/1.0/round-([a-z0-9]+).json", round_.Handler),
        (r"/1.0/round_activity-([a-z0-9]+).json", round_.ActivityHandler),
        (r"/1.0/user-([a-z0-9]+)/stream.json", user.StreamHandler),
        (r"/1.0/user-([a-z0-9]+)/(follow|unfollow).json", user.SubscriptionHandler),
        (r"/1.0/user-([a-z0-9]+).json", user.Handler),
        (r"/1.0/__admin_hore/user.json", admin.UserHandler),
        (r"/1.0/__admin_hore/app.json", admin.AppHandler),
        (r"/1.0/__admin_hore/app_access.json", admin.AppAccessHandler),
        ]
    settings = dict()
    application = tornado.web.Application(handlers, **settings)
    application.listen(11002)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    

