from mongoengine import Document

class BaseModel(Document):
    '''
    classdocs
    '''
    meta = {'allow_inheritance': True}
