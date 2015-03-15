#coding=utf-8
from flask import session, jsonify, flash, redirect
from bson.errors import InvalidId
from functools import wraps

from core.baseConfig import CONST_ERROR_CODE_LOGINREQUIRED, CONST_ERROR_CODE_INALIDID
from core.baseResult import *

def valide_params(keys, params):
    for key in keys:
        if key not in params:
            return False
    return True

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not session.get('uid', None):
            return jsonify(baseJson(CONST_ERROR_CODE_LOGINREQUIRED, '需要登录')), 403
        else:
            return func(*args, **kwargs)
    return wrap

def login_required_web(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not session.get('uid', None):
            flash('请先登录')
            return redirect('/admin/login')
        else:
            return func(*args, **kwargs)
    return wrap
        

def base_auth_save(uid):
    session['uid'] = uid
    
def base_auth_getUid():
    return session.get('uid', None)
    
def base_auth_logout():
    session.pop('uid', None)

def base_get_list(provider):
    objs = provider.load();
    result = baseJson()
    result['data'] =  objs
    return result, objs

def base_get_list_bypage(provider, start, num):
    objs = provider.loadByPage(start, num);
    result = baseJson()
    result['data'] =  objs
    return result, objs

def base_post_obj(provider, params):
    try:
        obj, msg = provider.create(params)
    except Exception, e:
        return baseJson(404, str(e)), None
    return baseJson(0 if obj is not None else 201, msg), obj

def base_get_obj(provider, oid):
    try:
        obj, msg = provider.loadById(oid)
    except InvalidId:
        return baseJson(CONST_ERROR_CODE_INALIDID, '用户ID不合法'), None
    except Exception, e:
        return baseJson(404, str(e)), None
    return baseJson(0 if obj is not None else 404, msg), obj

def base_put_obj(provider, oid, params):
    try:
        obj, msg = provider.updateById(oid, params)
    except InvalidId:
        return baseJson(CONST_ERROR_CODE_INALIDID, '用户ID不合法'), None
    except Exception, e:
        return baseJson(201, str(e)), None
    return baseJson(0 if obj is not None else 201, msg), obj

def base_delete_obj(provider, oid):
    try:
        obj, msg = provider.deleteById(oid)
    except InvalidId:
        return baseJson(CONST_ERROR_CODE_INALIDID, '用户ID不合法'), None
    except Exception, e:
        return baseJson(204, str(e)), None
    return baseJson(0 if obj is not None else 204, msg), obj