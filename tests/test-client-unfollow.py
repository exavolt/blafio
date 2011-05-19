
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
    print "usage: %s <target id>" % sys.argv[0]

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    uid = sys.argv[1]
    url = config.API_BASE_URL + 'user-' + uid + '/unfollow.json'
    values = dict(
        access_token=config.ACCESS_TOKEN
        )
    req = urllib2.Request(url, urllib.urlencode(values))
    act = None
    try:
        response = urllib2.urlopen(req)
        the_page = response.read()
        response.close()
        act = json.loads(the_page)
    except urllib2.HTTPError, http_err:
        print "Non-OK response: %d" % http_err.code
        if http_err.code == 201:
            the_page = http_err.read()
            act = json.loads(the_page)
        else:
            print http_err.read()
        http_err.close()
    if not act:
        print "Something's not right"
        return


if __name__ == "__main__":
    main()

