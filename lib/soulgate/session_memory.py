#!/usr/bin/env python

"""Process's memory session storage backend

As the name implies, this backend stores the session data in process's 
memory. Thus the sessions live as the application not exited and the sessions 
are not be shared among processes.

WARNING: This backend makes the application to take a lot of memory usage 
depending on the stored session.
"""

from datetime import datetime

from session_stub import *


class SessionStore(object):
    
    storage = dict()
    
    def __init__(self, **kwargs):
        pass
    
    def get_data(self, id):
        sdat = self.storage.get(id)
        if not sdat or sdat.get('deleted', False):
            raise DataNotFoundError()
        data = sdat.get('data', dict())
        sdat['accessed_datetime'] = datetime.utcnow()
        self.storage[id] = sdat #TODO: updated only
        return data
    
    def put_data(self, id, data):
        if data is not None and not isinstance(data, dict):
            raise ValueError("Data must be dict")
        tnow = datetime.utcnow()
        sdat = self.storage.get(id)
        if not sdat:
            self.storage[id] = dict(
                created_datetime=tnow,
                accessed_datetime=tnow,
                updated_datetime=None,
                data=data,
                deleted=False,
                deleted_datetime=None,
                )
            return True
        elif sdat.get('deleted', False):
            sdat['deleted'] = False
            sdat['data'] = None
        if data is not None:
            sdat['data'] = data
        sdat['accessed_datetime'] = tnow
        sdat['updated_datetime'] = tnow
        self.storage[id] = sdat
        return True
    
    def destroy(self, id):
        """Destroys a session (makes it non-retrievable)"""
        sdat = self.storage.get(id)
        if not sdat:
            return
        if not sdat.get('deleted', False):
            sdat['deleted'] = True
            sdat['deleted_datetime'] = datetime.utcnow()
            self.storage[id] = sdat
    

