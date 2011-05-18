#!/usr/bin/env python

#TODO: should be 'blafio.core.round_'
import core.round_

import base


class StreamHandler(base.RequestHandler):
    
    @base.oauth_method
    def get(self):
        data = []
        for act in core.round_.RoundActivity.objects.order_by('-timestamp')[:20]:#.all():
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

