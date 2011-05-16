
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


#API_BASE_URL = 'http://example.com:11002/1.0/'
API_BASE_URL = 'http://api.beta.blafio.com/1.0/'

#ACCESS_TOKEN = 'hwarakadahdehpokoknya001'
#ACCESS_TOKEN = 'Z55IIxkrRE04gu7YEss7dGLMwHAk09yQggf6PBdN' # Monkey (TestApp)
#ACCESS_TOKEN = 'NWihjTadF3peBLzf2uNNR05E6ywF3aOC5RkBdp7h' # Leopard (TestApp)
ACCESS_TOKEN = '8ZxACNjNVZCsMg5DfdULRZH4V9nJ70qeK8MudAP9' # BlackPanther (TestApp)

def print_usage():
    print "usage: %s [round name]" % sys.argv[0]

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    round_name = sys.argv[1]
    url = API_BASE_URL + 'round/start.json'
    values = dict(
        access_token=ACCESS_TOKEN,
        name=round_name
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
    
    print "Round started"
    #print repr(act)
    time.sleep(15) # in seconds
    
    url = API_BASE_URL + 'round/finish.json'
    values = dict(
        access_token=ACCESS_TOKEN,
        round=act['round']['id']
        )
    req = urllib2.Request(url, urllib.urlencode(values))
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

