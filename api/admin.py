#!/usr/bin/env python

import functools
import string
import random
from datetime import datetime
import logging

import tornado.web

#TODO: should be 'blafio.core.round_'
import core.user
import core.app

import base


ADMIN_TOKEN = 'apapundeh'


def administrator(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        access_token = self.get_arguments('access_token', None)
        if not access_token and access_token != ADMIN_TOKEN:
            logging.error("Invalid access token: " + str(access_token))
            raise tornado.web.HTTPError(404)
        return method(self, *args, **kwargs)
    return wrapper


class UserHandler(base.RequestHandler):
    
    @administrator
    def post(self):
        #TODO: Checks!!
        name = self.get_argument('name')
        idname = core.user.normalize_name(name)
        usr = core.user.User.objects(idname=idname).first()
        if not usr:
            usr = core.user.User(
                name=name,
                idname=idname
                )
            usr.save()
            self.send_json(201, usr.prep_dump(details=3))
            return
        self.send_json(200, usr.prep_dump(details=3))
    

class AppHandler(base.RequestHandler):
    
    @administrator
    def post(self):
        #TODO: Checks!!
        name = self.get_argument('name')
        idname = core.app.normalize_name(name)
        secret = self.get_argument('secret', None) or \
            ''.join(random.choice(string.ascii_letters + string.digits) 
                    for x in range(40))
        app = core.app.App.objects(idname=idname).first()
        if not app:
            app = core.app.App(
                name=name,
                idname=idname,
                secret=secret
                )
            app.save()
            self.send_json(201, app.prep_dump(details=3))
            return
        if self.get_argument('secret', None):
            app.secret = secret
            app.save()
        self.send_json(200, app.prep_dump(details=3))
    

class AppAccessHandler(base.RequestHandler):
    
    @administrator
    def post(self):
        #TODO: Checks!!
        user_name = core.user.normalize_name(self.get_argument('user_name'))
        app_name = core.app.normalize_name(self.get_argument('app_name'))
        usr = core.user.User.objects(idname=user_name).first()
        app = core.app.App.objects(idname=app_name).first()
        token = self.get_argument('token', None) or \
            ''.join(random.choice(string.ascii_letters + string.digits) 
                    for x in range(40)) #TODO: Meaningful token
        access = core.app.AppAccess.objects(user=usr, app=app).first()
        if not access:
            access = core.app.AppAccess(
                user=usr,
                app=app,
                token=token
                )
            access.save()
            self.send_json(201, access.prep_dump(details=3))
            return
        if self.get_argument('token', None):
            access.token = token
            access.save()
        self.send_json(200, access.prep_dump(details=3))
    

