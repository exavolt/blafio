#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json

import asyncmongo
import tornado.web


class RequestHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
        try:
            return self._db
        except:
            pass
        self._db = asyncmongo.Client(
            pool_id='mydb',
            host='127.0.0.1',
            port=27017,
            maxcached=10,
            maxconnections=50,
            dbname='blafio'
            )
        return self._db
    
    def respond_json(self, status, json_data):
        self.set_status(status)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(json_data))
    

