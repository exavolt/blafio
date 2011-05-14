#!/usr/bin/env python

import sys
import os.path
import daemon

class Daemon(daemon.Daemon):
    
    def run(self):
        import main
        main.main()

if __name__ == "__main__":
    d = Daemon(
        pidfile='/tmp/blafio-web.pid', 
        stdout='/tmp/blafio-web.out',
        stderr='/tmp/blafio-web.err'
        )
    #d.base_path = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            d.start()
        elif 'stop' == sys.argv[1]:
            d.stop()
        elif 'restart' == sys.argv[1]:
            d.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    

