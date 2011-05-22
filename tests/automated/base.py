

import sys
import time
import urllib
import urllib2
try:
    import json
except:
    import simplejson as json

import config


def add_user(name):
    url = config.ADMIN_API_BASE_URL + 'user.json'
    params = dict(
        access_token=config.ADMIN_ACCESS_TOKEN,
        name=name
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
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        return False, None
    if resp_data.get('error'):
        return False, resp_data
    return True, resp_data

def add_app(name):
    url = config.ADMIN_API_BASE_URL + 'app.json'
    params = dict(
        access_token=config.ADMIN_ACCESS_TOKEN,
        name=name
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
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        return False, None
    if resp_data.get('error'):
        return False, resp_data
    return True, resp_data

def add_app_user(app_name, user_name):
    url = config.ADMIN_API_BASE_URL + 'app_access.json'
    params = dict(
        access_token=config.ADMIN_ACCESS_TOKEN,
        user_name=user_name,
        app_name=app_name
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
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        return False, None
    if resp_data.get('error'):
        return False, resp_data
    return True, resp_data


def start_round(access_token, round_name):
    url = config.API_BASE_URL + 'round/start.json'
    params = dict(
        access_token=access_token,
        name=round_name
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
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        return False, None
    if resp_data.get('error'):
        return False, resp_data
    return True, resp_data

def finish_round(access_token, round_id):
    url = config.API_BASE_URL + 'round/finish.json'
    params = dict(
        access_token=access_token,
        round=round_id
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
        if http_err.code == 201:
            resp_body = http_err.read()
            resp_data = json.loads(resp_body)
        else:
            print http_err.read()
        http_err.close()
    if not resp_data:
        return False, None
    if resp_data.get('error'):
        return False, resp_data
    return True, resp_data

