#!/usr/bin/env python

try:
    import json
except:
    import simplejson as json
from datetime import datetime
import logging

#TODO: should be 'blafio.core.round_'
#import core.round_

import pymongo.objectid
import tornado.web
import base

#TEMP
SUPPORTED_ACTIONS = [
    'start',
    'reset', # Bail out
    'finish', # Time out
    'interrupt', 
    'resume'
    ]


class ActionHandler(base.RequestHandler):
    
    @tornado.web.asynchronous
    def post(self, action):
        if action not in SUPPORTED_ACTIONS:
            self.respond_json(400, dict(
                message="Invalid round action"
                ))
            return
        rd_id = self.get_argument('round', None)
        if action != 'start' and rd_id is None:
            self.respond_json(400, dict(
                message="Round identifier not provided"
                ))
            return
        def _do_activity_insert(rd_data):
            rd_act_id = pymongo.objectid.ObjectId()
            def _activity_insert_cb(data, error):
                if error:
                    logging.error("Round activity insert error: " + str(error))
                    self.respond_json(500, dict(
                        message="Internal server error"
                        ))
                    self.finish()
                    return
                if not data or not len(data):
                    logging.error("Round activity insert failed")
                    self.respond_json(500, dict(
                        message="Internal server error"
                        ))
                    self.finish()
                    return
                def _activity_find_cb(resp, error):
                    if errror:
                        logging.error("Round activity find error: " + str(error))
                        self.respond_json(500, dict(
                            message="Internal server error"
                            ))
                        return
                    if not data or not len(data):
                        # This should never happen
                        logging.error("Round activity not found")
                        self.respond_json(500, dict(
                            message="Internal server error"
                            ))
                        return
                    self.respond_json(201, dict(
                        id=str(resp[0].get('_id')),
                        action=resp[0].get('action'),
                        timestamp=resp[0].get('timestamp').isoformat(),
                        round=dict(
                            id=str(rd_data.get('_id')),
                            name=rd_data.get('name')
                            )
                        ))
                    self.finish()
                self.db.RoundActivity.find({'_id': rd_act_id}, limit=1, 
                    callback=_activity_find_cb)
            self.db.RoundActivity.insert(dict(
                _id=rd_act_id,
                round=rd_data.get('_id'),
                action=action,
                timestamp=datetime.utcnow()
                ), callback=_activity_insert_cb)
        def _do_round_find(oid):
            def _round_find_cb(resp, error):
                if not resp or not len(resp):
                    self.respond_json(404, dict(message="Round not found"))
                    self.finish()
                    return
                #TODO: Check ownership
                _do_activity_insert(resp[0])
            self.db.Round.find({'_id': oid}, limit=1, 
                callback=_round_find_cb)
        if rd_id:
            rd_oid = None
            try:
                rd_oid = pymongo.objectid.ObjectId(rd_id)
            except:
                pass
            if not rd_oid:
                self.respond_json(400, dict(message="Invalid round identifier"))
                self.finish()
                return
            _do_round_find(rd_oid)
        else:
            rd_name = self.get_argument('name', None)
            rd_oid = pymongo.objectid.ObjectId()
            #TODO: If the name is not provided, take it from the task(s)
            #TODO: Tasks
            def _round_insert_cb(data, error):
                if error:
                    logging.error("Round insert error: " + str(error))
                    self.respond_json(500, dict(message="Internal server error"))
                    self.finish()
                    return
                if not data or not len(data):
                    logging.error("Round insert failed")
                    self.respond_json(500, dict(message="Internal server error"))
                    self.finish()
                    return
                _do_round_find(rd_oid)
            self.db.Round.insert(dict(
                _id=rd_oid,
                user=None,
                name=rd_name
                ), callback=_round_insert_cb)
    

