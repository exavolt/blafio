
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
    print "usage: %s <round name>" % sys.argv[0]

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    round_name = sys.argv[1]
    url = config.API_BASE_URL + 'round/start.json'
    params = dict(
        access_token=config.ACCESS_TOKEN,
        name=round_name
        )
    req = urllib2.Request(url, urllib.urlencode(params))
    resp_data = None
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
    
    print "Round started"
    #print repr(resp_data)
    time.sleep(1500) # in seconds
    
    url = config.API_BASE_URL + 'round/finish.json'
    params = dict(
        access_token=config.ACCESS_TOKEN,
        round=resp_data['round']['id']
        )
    req = urllib2.Request(url, urllib.urlencode(params))
    try:
        response = urllib2.urlopen(req)
        #print response.read()
        response.close()
    except urllib2.HTTPError, http_err:
        print "Non-OK response: %d" % http_err.code
        #print http_err.read()
        http_err.close()
    print "Round finished"


if __name__ == "__main__":
    main()

