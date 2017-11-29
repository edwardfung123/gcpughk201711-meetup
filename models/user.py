#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from google.appengine.ext import ndb

class User(ndb.Model):
  ctime = ndb.DateTimeProperty(auto_now_add=True)
  mtime = ndb.DateTimeProperty(auto_now=True)
  name = ndb.StringProperty(required=True, indexed=True)


  def to_dict(self, *args, **kwargs):
    ''' Override the default to_dict() so that i can return the `id` as well. '''
    ret = super(User, self).to_dict(*args, **kwargs)
    logging.debug(self.key.id())
    ret['id'] = self.key.id()
    return ret
