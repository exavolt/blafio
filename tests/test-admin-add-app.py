
# To test the API's very basic functionality.
# NOTE: Adjust the URLs before use


import sys
import time
import urllib
import urllib2
try:
    import json
except:
    import simplejson as json

import config


def print_usage():
    print "usage: %s <user name>" % sys.argv[0]

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    uname = sys.argv[1]
    url = config.ADMIN_API_BASE_URL + 'app.json'
    params = dict(
        access_token=config.ADMIN_ACCESS_TOKEN,
        name=uname
        )
    req = urllib2.Request(url, urllib.urlencode(params))
    resp_data = None
    resp_body = None
    try:
        response = urllib2.urlopen(req)
        resp_body = response.read()
        response.close()
        resp_data = json.loads(resp_body)
    except urllib2.HTTPError, http_err:
        print "Non-OK response: %d" % http_err.code
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        print "Something's not right"
        return
    if resp_body:
        print resp_body


if __name__ == "__main__":
    main()

