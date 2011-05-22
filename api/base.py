#!/usr/bin/env python

import httplib
import logging
import functools
try:
    import json
except:
    import simplejson as json

import tornado.web


class RequestHandler(tornado.web.RequestHandler):
    
    # Override to disable xsrf checks
    def check_xsrf_cookie(self):
        pass
    
    # Override
    def send_error(self, status_code=500, **kwargs):
        if self._headers_written:
            logging.error("Cannot send error response after headers written")
            if not self._finished:
                self.finish()
            return
        self.clear()
        self.set_status(status_code)
        self.set_header('Content-Type', 'application/json')
        data = dict(code=status_code, message='')
        if kwargs.get('exception'):
            e = kwargs['exception']
            if isinstance(e, HTTPError):
                data['message'] = e.message
            else:
                data['message'] = httplib.responses[status_code] #str(e)
        self.finish(json.dumps(data))
    
    def send_json(self, status_code, json_data):
        self.set_status(status_code)
        self.set_header('Content-Type', 'application/json')
        indent = None
        if self.get_argument('pretty_response', None):
            try:
                indent = int(self.get_argument('pretty_response'))
            except:
                indent = 4
        self.finish(json.dumps(json_data, indent=indent))
    

class HTTPError(tornado.web.HTTPError):
    
    def __init__(self, status_code, message, log_message=None, *args):
        tornado.web.HTTPError.__init__(self, status_code, log_message, *args)
        self.message = message
    

#TODO: add parameter whether the authentication is required or not
def oauth_method(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        access_token = self.get_arguments('access_token', None)
        if not access_token:
            raise HTTPError(400, "Invalid OAuth request")
        #TODO: Get the consumer and the resource's owner
        return method(self, *args, **kwargs)
    return wrapper

