
#TODO!!! This file should contains only the main class.
# The main routine should only be imported on run

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import logging

import round_

import mongoengine
import daemon
import tornado.web
import tornado.ioloop


class Main(daemon.Daemon):
    
    def run(self):
        #mongoengine.connect('blafio')
        mongoengine.connect('blafio-dev', 
            host='flame.mongohq.com', 
            port=27100, 
            username='exavolt', 
            password='000000'
            )
        settings = dict()
        application = tornado.web.Application([
            (r"/1.0/round/([a-z]+)\.json", round_.ActionHandler),
            ], **settings)
        application.listen(11002)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    daemon = Main(
        pidfile='/tmp/blafio-api.pid', 
        stdout='/tmp/blafio-api.out',
        stderr='/tmp/blafio-api.err'
        )
    daemon.base_path = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    

