
#TODO!!! This file should contains only the main class.
# The main routine should only be imported on run

import os.path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import string
import logging

import core.round_

import tornado.web


def datetime_timeago_abbr(dt):
    #TODO: i18n-l10n and user's preference
    return '<abbr class="timeago" title="%s">%s</abbr>' % (
        dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        dt.strftime("%A, %d %B %Y %H:%M GMT"),
        )
    


class StreamHandler(tornado.web.RequestHandler):
    
    def get(self):
        #TODO: Different template for each action type
        #TODO: i18n-L10n
        tpl = string.Template('<li>'
            '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
            '${action}ed working on <span class="task">\'${task_name}\'</span> '
            '${timestamp}</li>'
            )
        self.write('''\
<script src="/static/jquery-1.6.1.min.js" type="text/javascript"></script>
<script src="/static/jquery.timeago.js" type="text/javascript"></script>
<script type="text/javascript">
jQuery(document).ready(function() {
  jQuery("abbr.timeago").timeago();
});
</script>
''')
        self.write('<h2>Stream</h2>\n')
        self.write('<ul>')
        for act in core.round_.RoundActivity.objects.order_by('-timestamp'):
            #TODO: HTML escape
            self.write(tpl.substitute(
                actor_url="",
                actor_name='someone',
                action=act.action,
                task_name=act.round_.name,
                timestamp=datetime_timeago_abbr(act.timestamp)
                ))
        self.write('</ul>\n')
    

class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write("Hello, world")
    


import mongoengine
import daemon
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
        logging.warn(os.path.join(self.base_path, "static"))
        settings = dict(
            static_path=os.path.join(self.base_path, "static"),
            )
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/stream", StreamHandler),
            ], **settings)
        application.listen(11003)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    daemon = Main(
        pidfile='/tmp/blafio-web.pid', 
        stdout='/tmp/blafio-web.out',
        stderr='/tmp/blafio-web.err'
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
    

