from pymongo import MongoClient
from core.baseConfig import *

CONST_SERVER_NAME = 'fighting'

client = MongoClient('127.0.0.1', 27017)
db = client['fighting']