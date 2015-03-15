#coding=utf-8
from flask import Flask, jsonify, Blueprint, make_response, request, session
from flask.ext.restful import reqparse, abort, Api, Resource
from mongoengine import *

from core.baseAPI import *
from provider.userProvider import UserProvider
from config import *

app = Flask(CONST_SERVER_NAME)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('password', type=str)
parser.add_argument('mobile', type=str)
parser.add_argument('email', type=str)

userProvider = UserProvider()

user_api = Blueprint('user_api', __name__)

@user_api.route('api/user/login', methods = ['POST'])
def users_login():
    args = parser.parse_args()
    if not valide_params(['name','password'],args):
        return jsonify(baseJson(CONST_ERROR_CODE_INVALIDPARAM, '用户名和密码不能为空'))
    obj, msg = userProvider.login(args['name'], args['password'])
    if obj is None:
        return jsonify(baseJson(501, msg))
    base_auth_save(obj['oid'])
    result = baseJson()
    result['user'] = obj
    return jsonify(result)

@user_api.route('/api/user/logout', methods = ['GET', 'POST'])
def users_logout():
    base_auth_logout()
    return jsonify(baseJson())
  
@user_api.route('/api/users', methods = ['POST'])
def users_post():
    args = parser.parse_args()
    result, obj = base_post_obj(userProvider,args)
    if obj is not None:
        result['user'] = obj
    return jsonify(result), 201  

@user_api.route('/api/users/<string:oid>', methods = ['GET'])
@login_required
def user_get(oid):
    result, obj = base_get_obj(userProvider,oid)
    if obj is not None:
        result['user'] = obj
    return jsonify(result), 404

@user_api.route('/api/users/<string:oid>', methods = ['PUT'])
@login_required
def user_put(oid):
    if base_auth_getUid() != oid:
        return jsonify(baseJson(CONST_ERROR_CODE_INVALIDPARAM, '只能修改本人的用户信息'))
    args = parser.parse_args()
    result, msg = base_put_obj(userProvider,oid,args)
    return jsonify(result), 201

@user_api.route('/api/users/<string:oid>', methods = ['DELETE'])
@login_required
def user_delete(oid):
    if base_auth_getUid() != oid:
        return jsonify(baseJson(CONST_ERROR_CODE_INVALIDPARAM, '只能删除本人的用户信息'))
    result, msg  = base_delete_obj(userProvider,oid)
    return jsonify(result), 204
   
if __name__ == '__main__':
    app.run(debug=True)