#!/usr/bin/env python

import string
import blafiocore.round_
import tornado.web


def datetime_timeago_abbr(dt):
    #TODO: i18n-l10n and user's preference
    return '<abbr class="timeago" title="%s">%s</abbr>' % (
        dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        dt.strftime("%A, %d %B %Y %H:%M GMT"),
        )
    
#TODO: Different template for each action type
#TODO: i18n-L10n
activity_templates = dict()
activity_templates['start'] = string.Template('<li><div>'
    '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
    'started <span class="round">"${round_name}"</span> '
    '${timestamp}</div></li>'
    )
activity_templates['finish'] = string.Template('<li><div>'
    '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
    'finished <span class="round">"${round_name}"</span> '
    '${timestamp}</div></li>'
    )
activity_templates['reset'] = string.Template('<li><div>'
    '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
    'cancelled <span class="round">"${round_name}"</span> '
    '${timestamp}</div></li>'
    )
activity_templates['interrupt'] = string.Template('<li><div>'
    '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
    'interrupted <span class="round">"${round_name}"</span> '
    '${timestamp}</div></li>'
    )
activity_templates['resume'] = string.Template('<li><div>'
    '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
    'resumed <span class="round">"${round_name}"</span> '
    '${timestamp}</div></li>'
    )


class ViewHandler(tornado.web.RequestHandler):
    
    def get(self):
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
        for act in blafiocore.round_.RoundActivity.objects.order_by('-timestamp')[:20]:#.all():
            tpl = activity_templates[act.action]
            #TODO: HTML escape
            self.write(tpl.substitute(
                actor_url="/u/" + act.actor.name,
                actor_name=act.actor.name,
                action=act.action,
                round_name=act.round_.name,
                timestamp=datetime_timeago_abbr(act.timestamp)
                ))
        self.write('</ul>\n')
    

