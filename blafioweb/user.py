#!/usr/bin/env python

import string
import blafiocore.user
import blafiocore.round_
import tornado.web


def datetime_timeago_abbr(dt):
    #TODO: i18n-l10n and user's preference
    return '<abbr class="timeago" title="%s">%s</abbr>' % (
        dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        dt.strftime("%A, %d %B %Y %H:%M GMT"),
        )
    


class Handler(tornado.web.RequestHandler):
    
    def get(self, uname):
        idname = blafiocore.user.normalize_name(uname)
        usr = blafiocore.user.User.objects(idname=idname).first()
        if not usr:
            raise tornado.web.HTTPError(404, "User '" + uname + "' is not found")
        #TODO: Different template for each action type
        #TODO: i18n-L10n
        tpl = string.Template('<li><div>'
            '<span class="actor"><a href="${actor_url}">${actor_name}</a></span> '
            '${action}ed working on <span class="round">"${round_name}"</span> '
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
        self.write('<h1>%s</h1>\n' % usr.name)
        act = blafiocore.round_.RoundActivity.objects(actor=usr).order_by('-timestamp').first()
        if act:
            if act.action == 'finish':
                self.write('<p>Taking a break after "%s" from %s.</p>\n' % (
                    act.round_.name, datetime_timeago_abbr(act.timestamp)))
            #elif act.action == 'start':
            else:
                self.write('<p>Working on "%s" from %s.</p>\n' % (
                    act.round_.name, datetime_timeago_abbr(act.timestamp)))
            self.write('<p><a href="/u/%s/follow">+ Follow</a></p>\n' % usr.name)
        self.write('<h2>Stream</h2>\n')
        self.write('<ul>')
        for act in blafiocore.round_.RoundActivity.objects(actor=usr).order_by('-timestamp')[:20]:#.all():
            #TODO: HTML escape
            self.write(tpl.substitute(
                actor_url="/u/" + act.actor.name,
                actor_name=act.actor.name,
                action=act.action,
                round_name=act.round_.name,
                timestamp=datetime_timeago_abbr(act.timestamp)
                ))
        self.write('</ul>\n')
    

