#!/usr/bin/env python

import urllib

import session


class Error(Exception):
    pass


_auth_service = None


#TODO: allow object for backend param
#TODO: check the auth service param (allow both dict and object)
def connect(backend, auth_service, **kwargs):
    global _auth_service
    if backend == 'memory':
        import session_memory
        session.storage = session_memory.SessionStore()
    elif backend == 'memcache':
        import session_memcache
        session.storage = session_memcache.SessionStore(
            host=kwargs.get('host', None), 
            port=kwargs.get('port', None)
            )
    elif backend == 'redis':
        import session_redis
        session.storage = session_redis.SessionStore(
            host=kwargs.get('host', None), 
            port=kwargs.get('port', None)
            )
    elif backend == 'mongodb':
        import session_mongodb
        session.storage = session_mongodb.SessionStore(
            host=kwargs.get('host', None), 
            port=kwargs.get('port', None)
            )
    elif backend == 'appengine':
        import session_appengine
        session.storage = session_appengine.SessionStore()
    elif backend == 'soullive':
        #TODO: the flow for soullive:
        # * connect to the master server (as provided)
        # * the returns are: status, auth_uri
        # * params: host, port, client_id, client_secret, auth_callback (as consumer)
        import session_soullive
        session.storage = session_soullive.SessionStore(
            host=kwargs.get('host', None), 
            port=kwargs.get('port', None)
            )
    else:
        #TODO: Possibilty to dynamically load the module and pass the 
        # params to it
        raise Error("Unsupported backend")
    #TODO: Exception if the handler is invalid
    _auth_service = auth_service
    

def create_signup_url(dest_url=None):
    try:
        return _auth_service.get_signup_url(dest_url)
    except AttributeError: #TODO: Filter the exceptions
        raise Error("SoulGate was not initialized properly")

def create_login_url(dest_url=None):
    try:
        return _auth_service.get_login_url(dest_url)
    except AttributeError: #TODO: Filter the exceptions
        raise Error("SoulGate was not initialized properly")

def create_logout_url(dest_url=None):
    try:
        return _auth_service.get_logout_url(dest_url)
    except AttributeError: #TODO: Filter the exceptions
        raise Error("SoulGate was not initialized properly")

def create_dashboard_url():
    try:
        return _auth_service.get_dashboard_url()
    except AttributeError: #TODO: Filter the exceptions
        raise Error("SoulGate was not initialized properly")
    

