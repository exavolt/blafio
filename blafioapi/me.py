#!/usr/bin/env python

import blafiostream.core
import blafiooauth.core

import base


class HomeStreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, context):
        #HACK-begin
        app = None
        usr = None
        app_access = blafiooauth.core.Access.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.client
        #HACK-end
        stream = blafiostream.core.Stream.objects(owner=usr, publishing=False, context=context).first()
        if not stream:
            stream = blafiostream.core.Stream(owner=usr, publishing=False, context=context)
            stream.save()
        data = []
        for act in blafiostream.core.Entry.objects(stream=stream, 
          deleted=False).order_by('-published_datetime')[:20]:
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

class SelfStreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, context):
        #HACK-begin
        app = None
        usr = None
        app_access = blafiooauth.core.Access.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.client
        #HACK-end
        stream = blafiostream.core.Stream.objects(owner=usr, publishing=True, context=context).first()
        if not stream:
            stream = blafiostream.core.Stream(owner=usr, publishing=True, context=context)
            stream.save()
        data = []
        for act in blafiostream.core.Entry.objects(stream=stream, 
          deleted=False).order_by('-published_datetime')[:20]:
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

