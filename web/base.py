#!/usr/bin/env python

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
    

