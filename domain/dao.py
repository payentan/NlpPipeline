import json
import os
from domain.persist import *

class Node():
    def __init__(self, prev_node_list, software, algorithm, parameters, result):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result

class NodeText():
    NAME = 'text'
    def __init__(self):
        pass

    def load(self, id):
        node_list = NodeCol.objects(id=id)
        assert node_list.count() == 1
        n = node_list.first()
        self.software = n.software
        self.algorithm = n.algorithm
        self.parameters =  n.parameters 
        for tid in json.loads(n.result)[self.NAME]:
            text = TextCol.objects(id=tid)
            assert text.count() == 1
            for t in text:
                self.title = t.title
                self.content = t.content
                self.source = t.source
                self.author = t.author
                self.timestamp = t.timestamp
                break
            break

    def import_text(self, text):
        assert len(text) > 0
        t = TextCol()
        self.content = t.content = text
        self.title = self.source = self.author = ''
        t.save()

        n = NodeCol()
        n.worker = self.NAME
        self.software = self.algorithm = n.software = n.algorithm = 'input'
        self.parameters = n.parameters = '{}'
        self.result = n.result = str(t.id)
        
        n.save()

    def import_file(self, file_path):
        assert os.path.exists(file_path)
        t = TextCol()
        self.content = t.content = open(file_path).read()
        self.title = self.source = self.author = ''
        t.save()

        n = NodeCol()
        n.worker = self.NAME
        self.software = self.algorithm = n.software = n.algorithm = 'input'
        self.parameters = n.parameters = '{}'
        self.result = n.result = str(t.id)
        n.save()

class NodeSegment():
    NAME = 'segment'
    def __init__(self):
        pass 
    def save(self, prev_node_list=None, software=None, algorithm=None, 
                parameters=None, result=None, conv_term=None):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result

        node = NodeCol()
        node.worker = self.NAME
        node.software = software
        node.algorithm = algorithm
        node.parameters = json.dumps(parameters)
        term_list = []

        seqId = 0
        for term in result:
            seg = SegmentCol()
            seg.seqId = seqId
            seqId += 1
            (seg.word, seg.nature, seg.offset) = conv_term(term)
            seg.save()
            term_list.append(str(seg.id))

        node.result = json.dumps({term_list})
        node.save()

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()


class NodeDependency():
    NAME = 'dependency'
    def __init__(self):
        pass

    def save(self, prev_node_list=None, software=None, algorithm=None, 
                parameters=None, result=None, conv_term=None):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result

        node = NodeCol()
        node.worker = self.NAME
        node.software = software
        node.algorithm = algorithm
        node.parameters = json.dumps(parameters)
        term_list = []

        seqId = 0
        for term in result:
            dep = DependencyCol()
            dep.seqId = seqId
            seqId += 1
            (dep.word, dep.lemma, dep.pos, dep.tag, dep.dep, dep.deprel) = conv_term(term)
            dep.save()
            term_list.append(str(dep.id))

        node.result = json.dumps({term_list})
        node.save()

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()

class NodeEmbedding():
    NAME = 'embedding'
    def __init__(self):
        pass

    def save(self, prev_node_list=None, software=None, algorithm=None, 
                parameters=None, model=None, preModel=''):

        emb = EmbeddngCol()
        emb.model = model
        emb.preModel = preModel
        emb.save()

        node = NodeCol()
        node.worker = self.NAME
        node.software = software
        node.algorithm = algorithm
        node.parameters = json.dumps(parameters)
        node.result = str(emb.id)
        node.save()

class NlpContext():
    def __init__(self):
        self.text = NodeText()
        self.segment = NodeSegment()
        self.dependency = NodeDependency()
        self.embedding = NodeEmbedding()
