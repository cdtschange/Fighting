#coding=utf-8
from mongoengine import *
from pymongo import *
import json
from bson import json_util
from bson.json_util import dumps

from core.baseProvider import BaseProvider
from model.user import User
from config import *


class UserProvider(BaseProvider):
    
    def getCollection(self):
        return db['user']
    
    def hidenProperties(self):
        return ['password']
    
    
    def create(self, params):
        uparams = {}
        filters = ['name','password','gender','mobile','email','isadmin']
        if 'name' not in params or params['name'] is None:
            return None, '用户名不能为空'
        for key in params:
            if key in filters and params[key] is not None:
                if key == 'password':
                    uparams[key] = User.hash_password(params[key])
                    continue
                uparams[key] = params[key]
        isExist = self.isExistByName(params['name'])
        if isExist:
            return None, '用户名已存在'
        return super(UserProvider, self).create(uparams)
    
    
    def updateById(self, oid, params):
        uparams = {}
        filters = ['name','password','gender','mobile','email','isadmin']
        for key in params:
            if key in filters and params[key] is not None:
                if key == 'password':
                    uparams[key] = User.hash_password(params[key])
                    continue
                uparams[key] = params[key]
        return super(UserProvider, self).updateById(oid, uparams)
        
    def isExistByName(self, name):
        collection = self.getCollection()
        hp = {x:0 for x in self.hidenProperties()}
        hp = hp if len(hp) > 0 else None
        obj = collection.find_one({'name': name},hp)
        return obj is not None
    
    def login(self, name, password):
        collection = self.getCollection()
        hp = {x:0 for x in self.hidenProperties() if x != 'password'}
        hp = hp if len(hp) > 0 else None
        obj = collection.find_one({'name': name},hp)
        if obj is None:
            return None, '用户不存在'
        json = self.objToDictionary(obj)
        if 'password' not in json or not User.verify_password(password, json['password']):
            return None, '用户密码错误'
        collection.update({'name': name},{'$inc':{'loginCnt':1}})
        del json['password']
        return json, ''