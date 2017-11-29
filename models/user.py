#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from google.appengine.ext import ndb

class User(ndb.Model):
  ctime = ndb.DateTimeProperty(auto_now_add=True)
  mtime = ndb.DateTimeProperty(auto_now=True)
  name = ndb.StringProperty(required=True, indexed=True)
  followers = ndb.IntegerProperty(required=True, indexed=True, default=0)
  profile_pic_url_raw = ndb.StringProperty(indexed=False)
  profile_pic_url = ndb.StringProperty(indexed=False)
  profile_pic_blob_key = ndb.BlobKeyProperty()


  def to_dict(self, *args, **kwargs):
    ''' Override the default to_dict() so that i can return the `id` as well. '''
    ret = super(User, self).to_dict(*args, **kwargs)
    logging.debug(self.key.id())
    ret['id'] = self.key.id()
    return ret
