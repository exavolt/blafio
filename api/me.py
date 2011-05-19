#!/usr/bin/env python

import core.stream

import base


class StreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self):
        #HACK-begin
        app = None
        usr = None
        app_access = core.app.AppAccess.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.app
        #HACK-end
        stream = core.stream.Stream.objects(owner=usr, context='main').first()
        if not stream:
            stream = core.stream.Stream(
                owner=usr,
                context='main'
                )
            stream.save()
        data = []
        for act in core.stream.StreamItem.objects(stream=stream, deleted=False).order_by('-published_datetime')[:20]:
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

