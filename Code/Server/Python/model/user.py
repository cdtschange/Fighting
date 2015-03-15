from mongoengine import *
from passlib.apps import custom_app_context as pwd_context

from core.baseModel import BaseModel

class User(BaseModel):
    name = StringField(max_length=100, required=True)
    password = StringField()
    mobile = StringField()
    mobileChecked = IntField()
    email = StringField()
    emailChecked = IntField()
    picsrc = StringField()
    point = IntField()
    ip = StringField()
    deviceID = StringField()
    deviceType = StringField()
    nickName = StringField()
    realName = StringField()
    birthiday = IntField()
    memberGrade = IntField()
    lastLoginTime = IntField()
    loginCnt = IntField()
    gender = IntField()
    idCardType = IntField()
    idCardNo = StringField()
    address = StringField()
    province = StringField()
    city = StringField()
    district = StringField()
    postCode = StringField()
    
    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)
        
    @staticmethod
    def verify_password(password, password_hash):
        print pwd_context.encrypt(password)
        return pwd_context.verify(password, password_hash)