#!/usr/bin/env python

import blafiostream
import core.app

import base


class HomeStreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, context):
        #HACK-begin
        app = None
        usr = None
        app_access = core.app.AppAccess.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.app
        #HACK-end
        stream = blafiostream.Stream.objects(owner=usr, publishing=False, context=context).first()
        if not stream:
            stream = blafiostream.Stream(owner=usr, publishing=False, context=context)
            stream.save()
        data = []
        for act in blafiostream.StreamItem.objects(stream=stream, 
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
        app_access = core.app.AppAccess.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.app
        #HACK-end
        stream = blafiostream.Stream.objects(owner=usr, publishing=True, context=context).first()
        if not stream:
            stream = blafiostream.Stream(owner=usr, publishing=True, context=context)
            stream.save()
        data = []
        for act in blafiostream.StreamItem.objects(stream=stream, 
          deleted=False).order_by('-published_datetime')[:20]:
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

