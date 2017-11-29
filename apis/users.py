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
          'cursor': cursor.urlsafe(),
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


app = Flask(__name__)
app.debug = True
api.init_app(app)
