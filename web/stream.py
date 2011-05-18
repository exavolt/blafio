#!/usr/bin/env python

import string
import core.round_
import tornado.web


def datetime_timeago_abbr(dt):
    #TODO: i18n-l10n and user's preference
    return '<abbr class="timeago" title="%s">%s</abbr>' % (
        dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        dt.strftime("%A, %d %B %Y %H:%M GMT"),
        )
    


class ViewHandler(tornado.web.RequestHandler):
    
    def get(self):
        #TODO: Different template for each action type
        #TODO: i18n-L10n
        tpl = string.Template('<li><div>'
            '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
            '${action}ed working on <span class="task">"${round_name}"</span> '
            '${timestamp}</div></li>'
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
        self.write('<h1>Global Stream</h1>\n')
        self.write('<ul>')
        for act in core.round_.RoundActivity.objects.order_by('-timestamp')[:20]:#.all():
            #TODO: HTML escape
            self.write(tpl.substitute(
                actor_url="/u/" + act.actor.name,
                actor_name=act.actor.name,
                action=act.action,
                round_name=act.round_.name,
                timestamp=datetime_timeago_abbr(act.timestamp)
                ))
        self.write('</ul>\n')
    

