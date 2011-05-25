#!/usr/bin/env python

import urllib


class AuthServiceInfo(object):
    
    def __init__(self, prefix=None):
        self.prefix = prefix or ''
    
    def get_login_url(self, dest_url=None):
        if dest_url:
            return self.prefix +'login?next=' + urllib.quote(dest_url)
        return self.prefix +'login'
    
    def get_logout_url(self, dest_url=None):
        if dest_url:
            return self.prefix +'logout?next=' + urllib.quote(dest_url)
        return self.prefix +'logout'
    
    def get_signup_url(self, dest_url=None):
        if dest_url:
            return self.prefix +'signup?next=' + urllib.quote(dest_url)
        return self.prefix +'signup'
    
    def get_dashboard_url(self):
        return self.prefix +'dashboard'
    

