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

api = Api(doc='/apis/doc', prefix="/apis")


# @api.route('/users')
# class HelloWorld(Resource):
#   def get(self):
#     return {'hello': 'world'}

ig_user_resp_model = api.model('IgUserRespModel', {
  'name': fields.String(required=True, description='IG Username', example='nike'),
  })

ig_user_list_resp_model = api.model('IgUserListRespModel', {
  'results': fields.List(fields.Nested(ig_user_resp_model), description='A list of ig user'),
  })


ig_create_user_model = api.model('IgUserCreateUserModel', {
  'name': fields.String(required=True, description='IG Username', example='nike'),
  })


__users__ = {}


@api.route('/users')
class CreateListUsers(Resource):

  @api.marshal_with(ig_user_list_resp_model)
  def get(self):
    '''Return a list of IG users to be FOLLOWED...'''
    # TODO: fetch users from database
    users = __users__.values()
    return {
        'results': users,
        }

  @api.expect(ig_create_user_model, validate=True)
  @api.marshal_with(ig_user_resp_model)
  def post(self):
    '''Create a new IG to be followed.'''
    from flask import request
    data = request.json
    logging.debug(data)
    if data['name'] in __users__:
      abort(400, 'already added before.')
    __users__[data['name']] = data
    return __users__[data['name']]


@api.route('/users/<username>')
class GetUpdateDeleteUser(Resource):

  @api.marshal_with(ig_user_resp_model)
  def get(self, username):
    '''Get the user from database'''
    logging.debug(username)
    if username not in __users__:
      logging.debug('not found')
      abort(404, 'User not found')
    return __users__[username]


  def delete(self, username):
    logging.debug(username)
    if username not in __users__:
      logging.debug('not found')
      abort(404, 'User not found')
    __users__.pop(username)
    return None


app = Flask(__name__)
app.debug = True
api.init_app(app)
