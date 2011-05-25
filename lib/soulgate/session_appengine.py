#!/usr/bin/env python

from datetime import datetime
import cPickle

from google.appengine.ext import db

from session_stub import *


class SessionData(db.Model):
    @classmethod
    def kind(cls):
        return 'soulgate_'+ cls.__name__
    
    # The key name is the session ID
    created_datetime = db.DateTimeProperty(auto_now_add=True)
    accessed_datetime = db.DateTimeProperty(auto_now_add=True)
    updated_datetime = db.DateTimeProperty()
    data = db.BlobProperty()
    deleted = db.BooleanProperty(default=False)
    deleted_datetime = db.DateTimeProperty()


class SessionStore(object):
    
    def __init__(self, **kwargs):
        pass
    
    def get_data(self, id):
        sdat = SessionData.get_by_key_name(id)
        if sdat is None or sdat.deleted:
            raise DataNotFoundError()
        data = cPickle.loads(sdat.data)
        sdat.accessed_datetime = datetime.utcnow()
        sdat.save()
        return data
    
    def put_data(self, id, data):
        if data is not None and not isinstance(data, dict):
            raise ValueError("Data must be dict")
        tnow = datetime.utcnow()
        sdat = SessionData.get_by_key_name(id)
        if sdat is None:
            sdat = SessionData(
                key_name=str(id),
                created_datetime=tnow,
                accessed_datetime=tnow,
                updated_datetime=None,
                data=cPickle.dumps(data, protocol=2),
                deleted=False,
                deleted_datetime=None
                )
            sdat.save()
            return True
        elif sdat.deleted:
            sdat.deleted = False
            sdat.data = None
        if data is not None:
            # Here we assume that it will only be accessed by Python
            sdat.data = cPickle.dumps(data, protocol=2)
        sdat.accessed_datetime = tnow
        sdat.updated_datetime = tnow
        sdat.save()
        return True
    
    def destroy(self, id):
        """Destroys a session (makes it non-retrievable)"""
        sdat = SessionData.get_by_key_name(id)
        if sdat is None:
            #CHECK: raise exception?
            return
        sdat.deleted = True
        sdat.deleted_datetime = datetime.utcnow()
        sdat.save()
    

