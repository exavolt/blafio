#!/usr/bin/env python

import blafiocore.round_

import base


class Handler(base.RequestHandler):
    
    @base.oauth_method
    def get(self):
        data = []
        for act in blafiocore.round_.RoundActivity.objects.order_by('-timestamp')[:20]:#.all():
            data.append(act.prep_dump(details=2))
        self.send_json(200, dict(
            data=data,
            paging=dict()
            ))
    

