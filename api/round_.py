#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json
from datetime import datetime

#TODO: should be 'blafio.core.round_'
import core.round_

import base


class ActionHandler(base.RequestHandler):
    
    def post(self, action):
        if action not in core.round_.ACTIVITIES:
            self.respond_json(400, dict(message="Invalid round action"))
            return
        round_id = self.get_argument('round', None)
        if action != 'start' and round_id is None:
            self.respond_json(400, dict(message="Round identifier not provided"))
            return
        round_ = None
        if round_id:
            round_ = core.round_.Round.objects(id=round_id).first()
            if not round_:
                self.respond_json(404, dict(message="Round not found"))
                return
            #TODO: Check ownership
        else:
            round_name = self.get_argument('name', None)
            #TODO: If the name is not provided, take it from the task(s)
            #TODO: Tasks
            round_ = core.round_.Round(
                user=None, #TODO!!!
                name=round_name
                )
            round_.save()
        round_act = core.round_.RoundActivity(
            round_=round_,
            action=action,
            timestamp=datetime.utcnow()
            )
        round_act.save()
        self.respond_json(201, round_act.prep_json())
    

