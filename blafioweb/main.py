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

import index
import stream
import user

import mongoengine
import tornado.httpserver
import tornado.web
import tornado.ioloop

from tornado.options import define, options


define("config", default=None, help="Config file name to load")
define("daemon", default=False, help="Run as daemon", type=bool)
define("host", default="", help="Listen to the specified host")
define("port", default=11001, help="Run on the given port", type=int)
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
        (r"/", index.ViewHandler),
        (r"/stream", stream.ViewHandler),
        (r"/u/([A-Za-z0-9_]+)", user.Handler),
        ]
    settings = dict(
        static_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 
            "static"),
        )
    
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
    if options.config:
        tornado.options.parse_config_file(options.config)
        # Parse the command line again to check the overrides
        tornado.options.parse_command_line()
    else:
        try:
            tornado.options.parse_config_file("./config.py")
            # Parse the command line again to check the overrides
            tornado.options.parse_command_line()
        except IOError:
            pass
        except:
            raise
    if options.daemon:
        # Capture stdout/err in logfile
        log_fname = '/tmp/blafioweb-%s.log' % options.port
        log_file = open(log_fname, 'a+')
        # Check pidfile
        pidfile = '/tmp/blafioweb-%s.pid' % options.port
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
    

