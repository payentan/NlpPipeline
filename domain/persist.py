from mongoengine import *
import datetime

connect('nlppipeline')

class Node(Document):
    parents = StringField(required=True)
    software = StringField(required=True)
    algorithm = StringField(required=True)
    parameter = StringField()
    result = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

class Text(Document):
    title = StringField()
    content = StringField(required=True)
    source = StringField()
    author = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class Segment(Document):
    seq_id = IntField(required=True)
    word = StringField(required=True)
    nature = StringField(required=True)
    offset = IntField()
    timestamp = DateTimeField(default=datetime.datetime.now)
