#!/usr/bin/env python

from tornado.web import RequestHandler as _RequestHandler
import soulgate.session


#TODO: move this somewhere (configurable)
_account_session_namespace = 'soulgate_account'
_cookie_name = 'soulgate.session'


# Override
def get_current_user(self):
    if self.session is None:
        return None
    if not self.session.is_active():
        self.clear_cookie(_cookie_name)
        return None
    #TODO: Support for anonymous session
    key_prefix = _account_session_namespace + '_'
    sdata = dict()
    for k in self.session.keys():
        if k.startswith(key_prefix):
            sdata[k[len(key_prefix):]] = self.session[k]
    if sdata.get('id') is None:
        #self.clear_session()
        return None
    return sdata

def set_current_user(self, data, clear_session=True):
    #CHECK: Save (dump) active session?
    if clear_session:
        # Simply (re)start the session
        self.session.start()
    for k, v in data.iteritems():
        self.session[_account_session_namespace +'_'+ k] = v

@property
def session(self):
    """Note that the session is empty (and will not be saved) before 
    you call session.start()
    """
    try:
        return self._session
    except AttributeError:
        self._session = self.get_session()
    except:
        self._session = None
    return self._session

def get_session(self):
    # Empty session
    sess = soulgate.session.Session()
    # Get the session ID from cookie
    sessid = self.get_secure_cookie(_cookie_name)
    # Load the session if the ID is valid. Otherwise, leave it empty
    if sessid:
        try:
            sess.load(sessid)
        except:
            self.clear_cookie(_cookie_name)
    return sess

# For logout (explicitly)
def clear_session(self):
    self.session.stop()
    self.clear_cookie(_cookie_name)
    delattr(self, '_session')
    
# Override
def finish(self, chunk=None):
    if hasattr(self, "_session"):
        if self._session.is_active():
            #TODO: check if the session is using auto-save mode
            self._session.save()
            sessid = self.get_secure_cookie(_cookie_name)
            if sessid != self._session.id:
                self.set_secure_cookie(_cookie_name, self._session.id)
        else:
            self.clear_cookie(_cookie_name)
    self._sg_orig_finish(chunk)


def monkey_patch(reqclass):
    if not hasattr(reqclass, '_sg_orig_finish'):
        reqclass.get_current_user = get_current_user
        reqclass.set_current_user = set_current_user
        reqclass.session = session
        reqclass.get_session = get_session
        reqclass.clear_session = clear_session
        reqclass._sg_orig_finish = reqclass.finish
        reqclass.finish = finish


class RequestHandler(_RequestHandler):
    pass

# Monkey patch it
monkey_patch(RequestHandler)


class AuthenticationCallbackHandler(RequestHandler):
    def get(self):
        self.require_setting("soulgate_client_id", "SoulGate auth")
        self.require_setting("soulgate_client_secret", "SoulGate auth")
        #TODO: check for authentication results (success, cancel, reject, error)
        error = self.get_argument('error', '')
        if error: #TODO: check the reason
            self.write("Authentication failed")
            self.set_status(500)
            return
        import soulgate.auth
        code = self.get_argument('code', '')
        sid = soulgate.auth.get_access_token(
            self.settings.get('soulgate_client_id'),
            self.settings.get('soulgate_client_secret'),
            code
            )
        #TODO: CHECKS
        self.set_secure_cookie(_cookie_name, sid)
        next_uri = self.get_argument('next', '')
        if not next_uri:
            next_uri = self.get_argument('continue', '')
        self.redirect(next_uri or '/')
    

