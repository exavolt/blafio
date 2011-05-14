#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json

import tornado.web


class RequestHandler(tornado.web.RequestHandler):
    
    def respond_json(self, status, json_data):
        self.set_status(status)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(json_data))

