#!/usr/bin/env python

#NOTE: Use ctl.py for serving this as daemon

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

import logging
import daemon
import pid

import me
import stream
import round_
import user
import admin

import mongoengine
import tornado.web
import tornado.ioloop

from tornado.options import define, options


define("host", default="127.0.0.1", help="listen to the specified host", type=str)
define("port", default=11002, help="run on the given port", type=int)
define("daemon", default=False, help="run as daemon", type=bool)


def run(pidfile=None):
    mongoengine.connect('blafio')
    # mongoengine.connect('blafio-dev', 
    #     host='flame.mongohq.com', 
    #     port=27100, 
    #     username='exavolt', 
    #     password='000000'
    #     )
    handlers = [
        (r"/1.0/home/stream/([A-Za-z0-9_]+).json", me.HomeStreamHandler),
        (r"/1.0/me/stream/([A-Za-z0-9_]+).json", me.SelfStreamHandler),
        (r"/1.0/stream.json", stream.Handler),
        (r"/1.0/round/(start|finish|reset|interrupt|resume).json", round_.Handler),
        (r"/1.0/round-([a-z0-9]+).json", round_.Handler),
        (r"/1.0/round_activity-([a-z0-9]+).json", round_.ActivityHandler),
        (r"/1.0/user-([a-z0-9]+)/stream.json", user.StreamHandler),
        (r"/1.0/user-([a-z0-9]+)/(follow|unfollow).json", user.SubscriptionHandler),
        (r"/1.0/user-([a-z0-9]+).json", user.Handler),
        (r"/1.0/__admin_hore/user.json", admin.UserHandler),
        (r"/1.0/__admin_hore/app.json", admin.AppHandler),
        (r"/1.0/__admin_hore/app_access.json", admin.AppAccessHandler),
        ]
    settings = dict()
    application = tornado.web.Application(handlers, **settings)
    application.listen(options.port)
    if pidfile:
        # write the pidfile
        pid.write(pidfile)
    try:
        # enter the Tornado IO loop
        tornado.ioloop.IOLoop.instance().start()
    finally:
        if pidfile:
            # ensure we remove the pidfile
            pid.remove(pidfile)
        print "Shutting down service..."
        tornado.ioloop.IOLoop.instance().stop()
    

def main():
    tornado.options.parse_command_line()
    if options.daemon:
        # Capture stdout/err in logfile
        log_file = '/tmp/blafioapi-%s.log' % options.port
        log = open(log_file, 'a+')
        # Check pidfile
        pidfile = '/tmp/blafioapi-%s.pid' % options.port
        pid.check(pidfile)
        # daemonize
        daemon_context = daemon.DaemonContext(
            stdout=log, 
            stderr=log, 
            working_directory='.'
            )
        with daemon_context:
            run(pidfile)
    else:
        try:
            run()
        except KeyboardInterrupt:
            print "Exit: KeyboardInterrupt"
    

if __name__ == "__main__":
    main()
    

