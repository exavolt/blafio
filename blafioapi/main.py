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
import tornado.httpserver
import tornado.web
import tornado.ioloop

from tornado.options import define, options


define("host", default="127.0.0.1", help="Listen to the specified host")
define("port", default=11002, help="Run on the given port", type=int)
define("daemon", default=False, help="Run as daemon", type=bool)
define("db_name", default="blafio", help="DB Name")
define("db_host", default=None, help="DB server address")
define("db_port", default=None, help="DB server port", type=int)
define("db_usr", default=None, help="DB username")
define("db_pwd", default=None, help="DB password")


def run(pidfile=None):
    mongoengine.connect(options.db_name,
        host=options.db_host,
        port=options.db_port,
        username=options.db_usr,
        password=options.db_pwd
        )
    
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
    #application = soulbox.web.Middleware(application)
    
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port, address=options.host)
    logging.info("Listening at %s:%i..." % (options.host, options.port))
    
    if pidfile:
        # Write the pidfile
        pid.write(pidfile)
    try:
        # Enter the Tornado IO loop
        tornado.ioloop.IOLoop.instance().start()
    finally:
        if pidfile:
            # Ensure we remove the pidfile
            pid.remove(pidfile)
        logging.info("Shutting down service...")
        tornado.ioloop.IOLoop.instance().stop()
    

def main():
    tornado.options.parse_command_line()
    if options.daemon:
        # Capture stdout/err in logfile
        log_fname = '/tmp/blafioapi-%s.log' % options.port
        log_file = open(log_fname, 'a+')
        # Check pidfile
        pidfile = '/tmp/blafioapi-%s.pid' % options.port
        pid.check(pidfile)
        # Daemonize
        daemon_context = daemon.DaemonContext(
            stdout=log_file, 
            stderr=log_file, 
            working_directory='.'
            )
        with daemon_context:
            run(pidfile)
    else:
        try:
            run()
        except KeyboardInterrupt:
            logging.info("Exit: KeyboardInterrupt")
    

if __name__ == "__main__":
    main()
    

