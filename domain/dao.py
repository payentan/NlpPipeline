import json
import os
from domain.persist import *

class Node(object):
    def __init__(self):
        pass

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def prev_node_list(self):
        return self._prev_node_list

    @prev_node_list.setter
    def prev_node_list(self, value):
        self._prev_node_list = value

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, value):
        self._software = value
    
    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
    
    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

class NodeText(Node):
    NAME = 'text'
    def __init__(self):
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
    
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
    
    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        self._author = value
    
    def load(self, id):
        node_list = NodeCol.objects(id=id)
        assert node_list.count() == 1

        n = node_list.first()
        self.id = str(n.id)
        self.software = n.software
        self.algorithm = n.algorithm
        self.parameters =  n.parameters 
        tid = n.result
        self._load(tid)

    def _load(self, tid):
        text = TextCol.objects(id=tid)
        if text.count() != 1:
            return 
        assert text.count() == 1
        t = text.first()
        self.title = t.title
        self.content = t.content
        self.source = t.source
        self.author = t.author

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

    def traverse(self, func):
        node_list = NodeCol.objects(worker=self.NAME)
        for node in node_list:
            self.load(node.id)
            func(self)

class NodeSegment(Node):
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

        node.result = " ".join(term_list)
        node.save()

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()

        print("")
        print("prev", prev_node_list)
        print("node", node.id)
        print(self.NAME, node.result)

class NodeDependency(Node):
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
        id_list = []

        seqId = 0
        for term in result:
            dep = DependencyCol()
            dep.seqId = seqId
            seqId += 1
            (dep.word, dep.lemma, dep.pos, dep.tag, dep.dep, dep.deprel) = conv_term(term)
            dep.save()
            id_list.append(str(dep.id))

        node.result = " ".join(id_list)
        node.save()

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()

        print("")
        print("prev", prev_node_list)
        print("node", node.id)
        print(self.NAME, node.result)

class NodeEmbedding(Node):
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

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()

        print("")
        print("prev", prev_node_list)
        print("node", node.id)
        print(self.NAME, node.result)

class NlpContext():
    def __init__(self):
        self.text = NodeText()
        self.segment = NodeSegment()
        self.dependency = NodeDependency()
        self.embedding = NodeEmbedding()
