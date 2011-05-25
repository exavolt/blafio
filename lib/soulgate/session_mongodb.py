#!/usr/bin/env python

"""MongoDB session storage backend (through the pymongo)
"""

from datetime import datetime

import pymongo

from session_stub import *


class SessionStore(object):
    
    #TODO: allow to use an existing connection
    def __init__(self, host=None, port=None, **kwargs):
        self.host = host
        self.port = port
    
    @property
    def connection(self):
        try:
            return self._connection
        except:
            self._connection = pymongo.Connection(self.host, self.port)
        return self._connection
    @property
    def collection(self):
        try:
            return self._collection
        except:
            self._collection = self.connection.soulgate.session
        return self._collection
    
    def get_data(self, id):
        sdat = self.collection.find_one({'_sg_sid': id})
        if not sdat or sdat.get('deleted', False):
            raise DataNotFoundError()
        data = sdat.get('data', {})
        sdat['accessed_datetime'] = datetime.utcnow()
        self.collection.save(sdat) #TODO: updated only
        return data
    
    def put_data(self, id, data):
        if data is not None and not isinstance(data, dict):
            raise ValueError("Data must be dict")
        tnow = datetime.utcnow()
        sdat = self.collection.find_one({'_sg_sid': id})
        if not sdat:
            sid = self.collection.insert(dict(
                _sg_sid=id,
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
        if data is not None:
            sdat['data'] = data
        sdat['accessed_datetime'] = tnow
        sdat['updated_datetime'] = tnow
        self.collection.save(sdat)
        return True
    
    def destroy(self, id):
        """Destroys a session (makes it non-retrievable)"""
        sdat = self.collection.find_one({'_sg_sid': id})
        if not sdat:
            return
        if not sdat.get('deleted', False):
            sdat['deleted'] = True
            sdat['deleted_datetime'] = datetime.utcnow()
            self.collection.save(sdat)
    

