#!/usr/bin/env python

import logging
import string

import pymongo
import tornado.web

import base


def datetime_timeago_abbr(dt):
    #TODO: i18n-l10n and user's preference
    return '<abbr class="timeago" title="%s">%s</abbr>' % (
        dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        dt.strftime("%A, %d %B %Y %H:%M GMT"),
        )
    


class ViewHandler(base.RequestHandler):
    
    @tornado.web.asynchronous
    def get(self):
        #TODO: Different template for each action type
        #TODO: i18n-L10n
        tpl = string.Template('<li class="round">'
            '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
            '${action}ed working on <span class="name">\'${round_name}\'</span> '
            '${timestamp}</li>'
            )
        def _round_activity_find_cb(resp, error):
            if error:
                logging.error("Round activity query error: " + str(error))
                raise tornado.web.HTTPError(500)
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
            #rd_set = set()
            for rd_act in resp:
                #rd_set.add(rd_act['round'].id)
                #TODO: HTML escape
                self.write(tpl.substitute(
                    actor_url="",
                    actor_name='someone',
                    action=rd_act['action'],
                    round_name=str(rd_act['round']),
                    timestamp=datetime_timeago_abbr(rd_act['timestamp'])
                    ))
            self.write('</ul>\n')
            self.finish()
        self.db.RoundActivity.find({}, limit=20, 
            sort=[('timestamp', pymongo.DESCENDING)],
            callback=_round_activity_find_cb)
    

