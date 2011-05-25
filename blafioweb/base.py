#!/usr/bin/env python

import os.path
import logging
import tornado.web

import soulgate.adapters.tornado
soulgate.adapters.tornado.monkey_patch(tornado.web.RequestHandler)


class RequestHandler(tornado.web.RequestHandler):
    pass

