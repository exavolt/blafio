#!/usr/bin/env python

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
import tornado.options
from tornado.options import options

import opts # Application's options


def setup_application():
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
    return application


def run(pidfile=None):
    mongoengine.connect(options.db_name,
        host=options.db_host,
        port=options.db_port,
        username=options.db_usr,
        password=options.db_pwd
        )
    
    http_server = tornado.httpserver.HTTPServer(setup_application())
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
        with daemon.DaemonContext(
            stdout=log_file, 
            stderr=log_file, 
            working_directory='.'
            ):
            run(pidfile)
    else:
        try:
            run()
        except KeyboardInterrupt:
            logging.info("Exit: KeyboardInterrupt")
    

if __name__ == "__main__":
    main()
    

