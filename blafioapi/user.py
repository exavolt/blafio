#!/usr/bin/env python

import blafiocore.round_
import blafiocore.user
import blafiostream

import base


class Handler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, u_id):
        #TODO: Level of details (also depends on the privilege)
        u_ref = blafiocore.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, error="invalid_user")
        u_data = u_ref.prep_dump(details=3)
        rd_ref = blafiocore.round_.RoundActivity.objects(actor=u_ref).order_by('-timestamp').first()
        if rd_ref:
            u_data['last_activity'] = rd_ref.prep_dump(details=2)
        #TODO: Check access
        self.send_json(200, u_data)
    

class StreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, u_id):
        #TODO: privilege
        u_ref = blafiocore.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, error="invalid_user")
        data = []
        for act in blafiocore.round_.RoundActivity.objects(actor=u_ref).order_by('-timestamp')[:20]:#.all():
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

class SubscriptionHandler(base.RequestHandler):
    
    @base.oauth_method
    def post(self, u_id, action):
        #TODO: Should disallow subcribing to self (it's always on)
        #HACK-begin
        app = None
        usr = None
        app_access = blafiooauth.core.Access.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.client
        #HACK-end
        if action not in ['follow', 'unfollow']:
            raise base.HTTPError(500, error="interal_server_error")
        u_ref = blafiocore.user.User.objects(id=u_id).first()
        if not u_ref:
            raise base.HTTPError(404, error="invalid_user")
        if u_ref.id == usr.id:
            raise base.HTTPError(403, error="invalid_subscription")
        subs = blafiocore.pubsub.Subscription.objects(
            subscriber=usr,
            publisher=u_ref).first()
        if action == 'follow':
            if not subs:
                subs = blafiocore.pubsub.Subscription(
                    subscriber=usr,
                    publisher=u_ref,
                    active=True,
                    pending=False
                    )
                subs.save()
                #HACK!!
                blafiostream.subscribe(usr, u_ref)
                self.send_json(201, subs.prep_dump(details=3))
                return
            if not subs.active:
                subs.active = True
                subs.save()
                #HACK!!
                blafiostream.subscribe(usr, u_ref)
            self.send_json(200, subs.prep_dump(details=3))
            return
        if subs and subs.active:
            subs.active = False
            subs.save()
            #HACK!!
            blafiostream.unsubscribe(usr, u_ref)
        self.send_json(200, dict())
            
    

