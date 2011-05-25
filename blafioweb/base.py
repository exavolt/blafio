#!/usr/bin/env python

import os.path
import logging
import tornado.web

import soulgate.adapters.tornado
soulgate.adapters.tornado.monkey_patch(tornado.web.RequestHandler)

import blafiocore.user


class RequestHandler(tornado.web.RequestHandler):
    
    # Override (again)
    def get_current_user(self):
        acc = super(RequestHandler, self).get_current_user()
        if not acc:
            return None
        usr = blafiocore.user.User.objects(account_id=acc['id']).first()
        if not usr:
            usr = blafiocore.user.User(
                account_id=acc['id'],
                name=acc['name'],
                idname=acc['name'] #TODO: Get this from the soulbox?
                )
            usr.save()
        else:
            #TODO: update if needed
            pass
        return usr
    

