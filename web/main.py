#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

import logging

import index
import stream
import user

import mongoengine
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
        )
    application = tornado.web.Application([
        (r"/", index.ViewHandler),
        (r"/stream", stream.ViewHandler),
        (r"/u/([A-Za-z0-9_]+)", user.Handler),
        ], **settings)
    application.listen(11001)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    

