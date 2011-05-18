#!/usr/bin/env python

import core.round_
import core.user
import core.subscription

import base


class Handler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, u_id):
        #TODO: Level of details (also depends on the privilege)
        u_ref = core.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, "User not found")
        u_data = u_ref.prep_dump(details=3)
        rd_ref = core.round_.RoundActivity.objects(actor=u_ref).order_by('-timestamp').first()
        if rd_ref:
            u_data['last_activity'] = rd_ref.prep_dump(details=2)
        #TODO: Check access
        self.send_json(200, u_data)
    

class StreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, u_id):
        #TODO: privilege
        u_ref = core.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, "User not found")
        data = []
        for act in core.round_.RoundActivity.objects(actor=u_ref).order_by('-timestamp')[:20]:#.all():
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

class SubscriptionHandler(base.RequestHandler):
    
    @base.oauth_method
    def post(self, u_id, action):
        #HACK-begin
        app = None
        usr = None
        app_access = core.app.AppAccess.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.app
        #HACK-end
        if action not in ['follow', 'unfollow']:
            raise base.HTTPError(500, "Assertion failed: invalid action")
        u_ref = core.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, "User not found")
        subs = core.subscription.Subscription.objects(
            subscriber=usr,
            publisher=u_ref).first()
        if action == 'follow':
            if not subs:
                subs = core.subscription.Subscription(
                    subscriber=usr,
                    publisher=u_ref,
                    active=True,
                    pending=False
                    )
                subs.save()
                self.send_json(201, subs.prep_dump(details=3))
                return
            if not subs.active:
                subs.active = True
                subs.save()
            self.send_json(200, subs.prep_dump(details=3))
            return
        if subs and subs.active:
            subs.active = False
            subs.save()
        self.send_json(200, dict())
            
    
