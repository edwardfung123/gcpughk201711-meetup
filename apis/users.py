#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is just a very very simple use case of flask-restplus.  To be somewhat
production ready, please use namespace and modularize your python scripts.  May
consider the memory footprint too.
'''

import logging
from flask import Flask
from flask_restplus import Api, Resource, fields, abort
from models.user import User

api = Api(doc='/apis/doc', prefix="/apis")


# @api.route('/users')
# class HelloWorld(Resource):
#   def get(self):
#     return {'hello': 'world'}

paginaton_model = api.model('PaginationModel', {
  'cursor': fields.String,
  'more': fields.Boolean,
  })

ig_user_resp_model = api.model('IgUserRespModel', {
  'name': fields.String(required=True, description='IG Username', example='nike'),
  'id': fields.Integer,
  'followers': fields.Integer,
  'profile_pic_url': fields.String,
  })

ig_user_list_resp_model = api.model('IgUserListRespModel', {
  'results': fields.List(fields.Nested(ig_user_resp_model), description='A list of ig user'),
  'pagination': fields.Nested(paginaton_model)
  })


ig_create_user_model = api.model('IgUserCreateUserModel', {
  'name': fields.String(required=True, description='IG Username', example='nike'),
  })


def get_user(username):
  user = User.query(User.name == username).get()
  return user


def is_user_exist(username):
  return get_user(username) is not None


@api.route('/users')
class CreateListUsers(Resource):

  @api.marshal_with(ig_user_list_resp_model)
  def get(self):
    '''Return a list of IG users to be FOLLOWED...'''
    from flask import request
    start_cursor = request.args.get('cursor', None)
    users, cursor, more = User.query().fetch_page(20, start_cursor=start_cursor)
    return {
        'results': [user.to_dict() for user in users],
        'pagination': {
          'cursor': cursor.urlsafe() if cursor is not None else None,
          'more': more,
          }
        }

  @api.expect(ig_create_user_model, validate=True)
  @api.marshal_with(ig_user_resp_model)
  def post(self):
    '''Create a new IG to be followed.'''
    from flask import request
    data = request.json
    logging.debug(data)
    # check user in the db first
    if is_user_exist(data['name']):
      abort(400, 'already added before.')
    user = User(**data)
    user.put()
    return user.to_dict()


@api.route('/users/<username>')
class GetUpdateDeleteUser(Resource):

  @api.marshal_with(ig_user_resp_model)
  def get(self, username):
    '''Get the user from database'''
    logging.debug(username)
    user = get_user(username)
    if user is None:
      logging.debug('not found')
      abort(404, 'User not found')
    return user.to_dict()


  def delete(self, username):
    logging.debug(username)
    user = get_user(username)
    if user is None:
      logging.debug('not found')
      abort(404, 'User not found')
    user.key.delete()
    return None


@api.route('/users/<username>/fetch')
class FetchIgUser(Resource):

  def get(self, username):
    logging.debug(username)
    user = get_user(username)
    if user is None:
      logging.debug('not found')
      abort(404, 'User not found')
    from utils.ig import fetchProfile, MissingIgUser, PrivateIgUser
    try:
      profile, sharedData, homepageHtml = fetchProfile(username)
    except PrivateIgUser:
      abort(400, 'The user is a private account!')
    except MissingIgUser:
      abort(400, 'The user does not exist in IG actually!')
    is_dirty = False
    if user.followers != profile['followed_by']['count']:
      user.followers = profile['followed_by']['count']
      is_dirty = True
    if profile['profile_pic_url_hd'] != user.profile_pic_url_raw:
      is_dirty = True
      user.profile_pic_url_raw = profile['profile_pic_url_hd']
      from google.appengine.api import urlfetch
      img_result = urlfetch.fetch(user.profile_pic_url_raw)
      if img_result.status_code == 200:
        img_content = img_result.content
      else:
        abort(400, 'Failed to download image')
      from google.appengine.api import images
      google_img = images.Image(img_content)
      if google_img.format == images.JPEG:
        content_type = 'image/jpeg'
        file_name = username + '.jpg'
      elif google_img.format == images.PNG:
        content_type = 'image/png'
        file_name = username + '.png'
      else:
        content_type = None
        file_name = username
      import cloudstorage as gcs
      from google.appengine.api import app_identity
      import os
      bucket_name = os.environ.get('BUCKET_NAME',
          app_identity.get_default_gcs_bucket_name())
      gcs_path = '/{bucket_name}/profile/{file_name}'.format(bucket_name=bucket_name,
          file_name=file_name)
      gcs_file = gcs.open(gcs_path, mode='w', content_type=content_type)
      gcs_file.write(img_content)
      gcs_file.close()

      from google.appengine.ext import blobstore
      blob_key = blobstore.create_gs_key('/gs'+gcs_path)
      url = images.get_serving_url(blob_key, secure_url=True)
      user.profile_pic_blob_key = blobstore.BlobKey(blob_key)
      user.profile_pic_url = url
    if is_dirty:
      user.put()
    return profile


app = Flask(__name__)
app.debug = True
api.init_app(app)
