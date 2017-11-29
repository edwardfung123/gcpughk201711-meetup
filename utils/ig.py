#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Good source https://github.com/kendricktan/iffse/blob/master/scrapper.py'''

import logging
import re
sharedDataJsonRegex = re.compile(r'_sharedData\s+=\s+(.*)</script>')

try:
  import ujson as json
  logging.debug('using ujson')
except ImportError:
  try:
    import simplejson as json
    logging.debug('using simplejson')
  except ImportError:
    import json
    logging.debug('using json')

from webob.exc import HTTPNotFound, HTTPServerError

def getHomeUrl(username):
  return r'https://www.instagram.com/{username}/?hl=en'.format(username=username)


def fetchHomePage(username):
  ''' Return the homepage HTML content of a user '''
  from google.appengine.api import memcache
  mkey = username
  homepage_content = memcache.get(key=mkey, namespace='ig-homepage')
  if homepage_content is not None:
    logging.debug('Cache hit!')
    return homepage_content

  logging.debug('cache miss')
  url = getHomeUrl(username)
  from google.appengine.api import urlfetch
  try:
    retries = 0
    delay = 1.0
    while retries < 5:
      result = urlfetch.fetch(url, method=urlfetch.GET, deadline=10)
      logging.debug('status_code = {}'.format(result.status_code))
      if result.status_code == 200:
        logging.debug('fetch the homepage')
        c = result.content
        # write to memcache
        added = memcache.set(key=mkey, value=c, time=60 * 60 * 24, namespace='ig-homepage')
        if not added:
          logging.error('Failed to cache the homepage')
          import sys
          logging.debug('Size = {} kb'.format(sys.getsizeof(c) / 1024))
        return c
      elif result.status_code == 404:
        e = HTTPNotFound('The account does not exist.')
        raise e
      elif result.status_code == 429:
        # this is the most tricky part. IG returns 429 for unknown reason...
        # wait for awhile and retry
        logging.debug('got 429... sleep awhile and retry afterward')
        import time
        time.sleep(delay)
        retries += 1
        delay *= 2
      else:
        logging.error(str(result))
        e = HTTPServerError('The server got an unexpected result from Instagram.')
        raise e
    raise HTTPServerError('Retried too many times')
  except urlfetch.Error:
    logging.error('Caught exception fetching url')
    raise
  except Exception as e:
    logging.exception(e)
    raise


def getSharedData(homepage_content):
  try:
    searchResult = sharedDataJsonRegex.search(homepage_content)
    if searchResult:
      jsonText = searchResult.group(1)[:-1]
      js = json.loads(jsonText)
      return js
    else:
      raise ValueError('Invalid result.')
  except Exception as e:
    logging.exception(e)
    raise


class MissingIgUser(Exception):
  pass


class PrivateIgUser(Exception):
  pass


def fetchProfile(username):
  homepage_content = fetchHomePage(username)
  sharedData = getSharedData(homepage_content)
  profiles = sharedData.get('entry_data', {}).get('ProfilePage', [])
  if profiles and len(profiles) == 0:
    raise MissingIgUser('The user does not exist.')
  igUser = profiles[0].get('user', {})
  if igUser.get('is_private', True) is True:
    raise PrivateIgUser('This is a private instagram account.')
  return igUser, sharedData, homepage_content
