#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

import round_

#import mongoengine
import tornado.web
import tornado.ioloop


def main():
    #mongoengine.connect('blafio')
    # mongoengine.connect('blafio-dev', 
    #     host='flame.mongohq.com', 
    #     port=27100, 
    #     username='exavolt', 
    #     password='000000'
    #     )
    settings = dict()
    application = tornado.web.Application([
        (r"/1.0/round/([a-z]+)\.json", round_.ActionHandler),
        ], **settings)
    application.listen(11002)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    

