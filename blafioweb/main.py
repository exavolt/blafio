#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

import logging

import index
import me
import stream
import user

import mongoengine
import soulbox
import soulgate
import tornado.web
import tornado.ioloop


def main():
    mongoengine.connect('blafio')
    # mongoengine.connect('blafio-dev', 
    #     host='flame.mongohq.com', 
    #     port=27100, 
    #     username='exavolt', 
    #     password='000000'
    #     )
    settings = dict(
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        cookie_secret='43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=', #TODO: Use different secret from the auth
        )
    application = tornado.web.Application([
        (r"/", index.ViewHandler),
        (r"/me", me.HomeHandler),
        (r"/stream", stream.ViewHandler),
        (r"/u/([A-Za-z0-9_]+)", user.Handler),
        ], **settings)
    application.listen(11001)
    soulgate.connect(backend='redis', 
        auth_service=soulbox.AuthServiceInfo('http://example.com:8888/account/'))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    

