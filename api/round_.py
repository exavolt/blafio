#!/usr/bin/env python

from datetime import datetime

#TODO: should be 'blafio.core.round_'
import core.round_
import mq

import base


class Handler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, rd_id):
        rd_ref = core.round_.Round.objects(id=rd_id).first()
        if not rd_ref:
            raise base.HTTPError(404, "Round not found")
        #TODO: Check access
        self.send_json(200, rd_ref.prep_dump(details=3))
    
    @base.oauth_method
    def post(self, action):
        #TODO: add optional parameter: duration
        #HACK-begin
        app = None
        usr = None
        app_access = core.app.AppAccess.objects(
            token=self.get_argument('access_token')).first()
        if app_access:
            usr = app_access.user
            app = app_access.app
        #HACK-end
        if action not in core.round_.ACTIONS:
            raise base.HTTPError(400, "Invalid round action")
        rd_id = self.get_argument('round', None)
        if action != 'start' and rd_id is None:
            raise base.HTTPError(400, "Round identifier not provided")
        rd_ref = None
        if rd_id:
            rd_ref = core.round_.Round.objects(id=rd_id).first()
            if not rd_ref:
                raise base.HTTPError(404, "Round not found")
            #TODO: Check ownership
        else:
            rd_name = self.get_argument('name', None)
            #TODO: If the name is not provided, take it from the task(s)
            #TODO: Tasks
            rd_ref = core.round_.Round(
                user=usr, #TODO!!!
                name=rd_name
                )
            rd_ref.save()
        rd_act = core.round_.RoundActivity(
            actor=usr,
            round_=rd_ref,
            action=action,
            timestamp=datetime.utcnow(),
            app=app
            )
        rd_act.save()
        mq.publish(usr, rd_act)
        self.send_json(201, rd_act.prep_dump(details=3))


class ActivityHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self, act_id):
        rd_act = core.round_.RoundActivity.objects(id=act_id).first()
        if not rd_act:
            raise base.HTTPError(404, "Round activity not found")
        #TODO: Check access
        self.send_json(200, rd_act.prep_dump(details=3))
    

