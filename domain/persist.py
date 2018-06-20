from mongoengine import *
import datetime

connect('nlppipeline')

class NodePreviousCol(Document):
    meta = {'collection': 'node_previus'}
    previousId = StringField(require=True)
    nodeId = StringField(require=True)

class NodeCol(Document):
    meta = {'collection': 'node'}
    worker = StringField(required=True)
    software = StringField(required=True)
    algorithm = StringField(required=True)
    parameters = StringField()
    result = StringField(require=True)
    timestamp = DateTimeField(default=datetime.datetime.now)

class TextCol(Document):
    meta = {'collection': 'text'}
    title = StringField()
    content = StringField(required=True)
    lang = StringField()
    source = StringField()
    author = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class SegmentCol(Document):
    meta = {'collection': 'segment'}
    seqId = IntField(required=True)
    word = StringField(required=True)
    nature = StringField(required=True)
    offset = IntField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class DependencyCol(Document):
    meta = {'collection': 'dependency'}
    seqId = IntField(required=True)
    word = StringField(required=True)
    lemma = StringField()
    pos = StringField()
    tag = StringField()
    dep = IntField()
    deprel = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class EmbeddngCol(Document):
    meta = {'collection': 'embedding'}
    preModel = StringField()
    texts = StringField()
    model = StringField()
    