#!/usr/bin/env python

import sys
import os.path

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib'))

import daemon


class Daemon(daemon.Daemon):
    
    def run(self):
        import main
        main.main()
    

if __name__ == "__main__":
    #TODO: parse the arguments after the command to be passed to the process
    base_filename = '/tmp/blafioapi' #TODO: get the port from the argv
    d = Daemon(
        pidfile=base_filename + '.pid', 
        stdout=base_filename + '.out',
        stderr=base_filename + '.err'
        )
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
    

