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
        for act in core.round_.RoundActivity.objects(actor=u_ref).order_by('-timestamp'):
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

class SubscriptionHandler(base.RequestHandler):
    
    @base.oauth_method
    def post(self):
        pass
    

