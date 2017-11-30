#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import webapp2


class Handler(webapp2.RequestHandler):
  def get(self):
    from google.appengine.api import taskqueue
    from models.user import User
    users = User.query()
    for user in users:
      url_path = '/apis/users/{}/fetch'.format(user.name)
      logging.debug(url_path)
      # default method is POST, but the API we defined only handle GET request.
      taskqueue.add(url=url_path, method='GET', payload=None)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hopefully we finished within 60s')


app = webapp2.WSGIApplication([
  (r'/tq/fetch_all_users', Handler),
  ], debug=True)
