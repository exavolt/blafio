#!/usr/bin/env python

import time
import datetime
import logging

import random
import string

from session_stub import *


#TODO: Generate cryptographically (non-deterministic) random unique id
def generate_id(prefix=''):
    #TODO: Prefixing
    return ''.join(random.choice(string.ascii_letters + string.digits) 
        for x in range(24))
    

#TODO: namespace for storage (set by application)
#TODO: Throw exception if the backend hasn't been set
#TODO!!! Clear session on session data set / get failures

storage = None


# This class acts as a proxy to the real session data
#Internal Note: if _data is None, it's not loaded yet; if empty, it's empty.
class Session(object):
    
    """The main session class"""
    def __init__(self, sid=None):
        self.storage = storage
        self.id = sid
        self._data = {}
        self.dirty = False
        self.lifetime = datetime.timedelta(days=7)
        if sid:
            self._data = None
    
    def is_active(self):
        return bool(self.id)
    
    def get(self, key, default=None):
        """Retrieves a value from the session."""
        return self.data.get(key, default)

    def items(self):
        return self.data.items()

    def iteritems(self):
        return self.data.iteritems()

    def keys(self):
        return self.data.keys()

    def iterkeys(self):
        return self.data.iterkeys()

    def has_key(self, key):
        return self.data.has_key(key)
    
    def __getitem__(self, key):
        """Returns the value associated with key on this session."""
        return self.data.__getitem__(key)
    
    def __setitem__(self, key, value):
        """Set a value named key on this session."""
        self.data.__setitem__(key, value) #CHECK: need to check if the data are different?
        self.dirty = True
    
    def __delitem__(self, key):
        self.data.__delitem__(key)
        self.dirty = True

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return self.data.has_key(key)

    def __iter__(self):
        for key in self.data:
            yield key
    
    def load(self, sid=None):
        #TODO: check if the session is expired
        if not sid and not self.id:
            logging.warning("Invalid session")
            raise InvalidError()
        if sid:
            self.id = sid
            self._data = None
    
    def save(self):
        if not self.id:
            logging.warning("Session not stored")
            return # Session is not active
        if not self.dirty or self._data is None:
            return # Nothing has changed
        #TODO: save the session head
        try:
            self.storage.put_data(self.id, self._data)
        except:
            #CHECK: Clear? Re-raise?
            raise
        self.dirty = False
    
    def start(self, expiration_ts=None):
        #TODO: expiration?
        # Request the backend for the ID
        self.id = generate_id()
        self.dirty = True
        self._data = {}
        logging.info('START %s' % self.id)
    
    def stop(self, destroy=True):
        """Deletes the session and its data, and expires the user's cookie."""
        logging.info('STOP %s' % self.id)
        #CHECK: save first?
        #TODO: flag the stored data as inactive
        if destroy and self.id and self.storage is not None:
            logging.info('DESTROY %s' % self.id)
            self.storage.destroy(self.id)
        self.id = None
        self._data = {}
        self.dirty = False
    
    @property
    def data(self):
        if self._data is None and self.id:
            # Fetch only the data, not included the session info (body, without the head)
            #TODO: stop the session if there's a failure in loading the data
            try:
                self._data = self.storage.get_data(self.id)
                self.dirty = False
            except DataNotFoundError:
                logging.warning("Data not found %s" % self.id)
                self.id = None
                self._data = {}
                self.dirty = False
            except Exception, e:
                logging.warning("%r %s" % (e, self.id))
                raise
        return self._data
    
    def __repr__(self):
        return '<%s.%s id=%r>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.id)
    
