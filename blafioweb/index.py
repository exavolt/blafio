#!/usr/bin/env python

import tornado.web


class ViewHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write('Hello, World!')
    

