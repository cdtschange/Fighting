#coding=utf-8
from flask import Flask
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import *


class BaseProvider(object):
    
    def hidenProperties(self):
        return []
    
    def getCollection(self):
        return None
    
    def objToDictionary(self, obj):
        data = json.loads(json.dumps(obj, default=json_util.default))
        if '_id' in data and '$oid' in data['_id']:
            data['oid'] = data['_id']['$oid']
            del data['_id']
        return data
    
    def loadById(self, oid):
        collection = self.getCollection()
        hp = {x:0 for x in self.hidenProperties()}
        hp = hp if len(hp) > 0 else None
        obj = collection.find_one({'_id': ObjectId(oid)},hp)
        if obj is None:
            return None, '获取失败'
        return self.objToDictionary(obj), ''
    
    def load(self):
        collection = self.getCollection()
        hp = {x:0 for x in self.hidenProperties()}
        hp = hp if len(hp) > 0 else None
        objs = collection.find({},hp)
        if objs is None:
            return []
        datas = []
        for obj in objs:
            data = self.objToDictionary(obj)
            datas.append(data)
        return datas
    
    def loadByPage(self, start = 0, num = 20):
        collection = self.getCollection()
        hp = {x:0 for x in self.hidenProperties()}
        hp = hp if len(hp) > 0 else None
        objs = collection.find({},hp).limit(num).skip(start)
        if objs is None:
            return []
        datas = []
        for obj in objs:
            data = self.objToDictionary(obj)
            datas.append(data)
        return datas
    
    def create(self, params):
        collection = self.getCollection()
        obj = collection.insert(params)
        if obj is None:
            return None, '创建失败'
        return self.objToDictionary(obj), ''
    
    def updateById(self, oid, params):
        if params is None or len(params) == 0:
            return None, '参数错误'
        collection = self.getCollection()
        obj = collection.update({'_id': ObjectId(oid)},{'$set':params})
        if obj is None:
            return None, '更新失败'
        if obj['updatedExisting'] == False:
            return None, 'ID不存在'
        if obj['ok'] != 1 or obj['n'] <= 0:
            return None, '更新失败'
        return self.objToDictionary(obj), ''
        
    def deleteById(self, oid):
        collection = self.getCollection()
        obj = collection.remove({'_id': ObjectId(oid)})
        if obj is None:
            return None, '删除失败'
        if obj['ok'] != 1 or obj['n'] <= 0:
            return None, '删除失败'
        return self.objToDictionary(obj), ''
    

    def isExistById(self, oid):
        return self.loadById(oid) is not None