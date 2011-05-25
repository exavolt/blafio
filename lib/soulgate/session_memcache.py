#!/usr/bin/env python

from datetime import datetime
from zlib import adler32

import memcache

import getset_bson
from session_stub import *


memcache.serverHashFunction = adler32
getset_bson.monkey_patch(memcache.Client)


class SessionStore(object):
    
    #TODO: allow to use an existing connection
    def __init__(self, host=None, port=None, key_prefix=None, **kwargs):
        self.host = host or '127.0.0.1'
        self.port = port or 11211
        self.key_prefix = key_prefix or 'soulgate.session-'
    
    @property
    def conn(self):
        try:
            return self._conn
        except:
            self._conn = memcache.Client([self.host + ':' + str(self.port)])
        return self._conn
    
    def get_data(self, id):
        sdat = self.conn.bson_get(self.key_prefix + id)
        if not sdat or sdat.get('deleted', False):
            raise DataNotFoundError()
        data = sdat.get('data', dict())
        sdat['accessed_datetime'] = datetime.utcnow()
        self.conn.bson_set(self.key_prefix + id, sdat) #TODO: updated only
        return data
    
    def put_data(self, id, data):
        if data is not None and not isinstance(data, dict):
            raise ValueError("Data must be dict")
        tnow = datetime.utcnow()
        sdat = self.conn.bson_get(self.key_prefix + id)
        if not sdat:
            self.conn.bson_set(self.key_prefix + id, dict(
                created_datetime=tnow,
                accessed_datetime=tnow,
                updated_datetime=None,
                data=data,
                deleted=False,
                deleted_datetime=None,
                ))
            return True
        elif sdat.get('deleted', False):
            sdat['deleted'] = False
            sdat['data'] = None
        #CHECK: Allow set the data to None? i.e. clear.
        if data is not None:
            sdat['data'] = data
        sdat['accessed_datetime'] = tnow
        sdat['updated_datetime'] = tnow
        self.conn.bson_set(self.key_prefix + id, sdat)
        return True
    
    def destroy(self, id):
        """Destroys a session (makes it non-retrievable)"""
        sdat = self.conn.bson_get(self.key_prefix + id)
        if not sdat:
            return
        if not sdat.get('deleted', False):
            sdat['deleted'] = True
            sdat['deleted_datetime'] = datetime.utcnow()
            self.conn.bson_set(self.key_prefix + id, sdat)
    

