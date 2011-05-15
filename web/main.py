#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

import index
import stream

import tornado.web
import tornado.ioloop


def main():
    settings = dict(
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        )
    application = tornado.web.Application([
        (r"/", index.ViewHandler),
        (r"/stream", stream.ViewHandler),
        ], **settings)
    application.listen(11001)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    

