import json
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
    def __init__(self, id):
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

class NodeSegment():
    NAME = 'segment'
    def __init__(self, prev_node_list, software, algorithm, parameters, result, conv_term):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result

        node = NodeCol()
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

        node.result = json.dumps({'segment' : term_list })
        node.save()

        nodePrev = NodePreviousCol()
        nodePrev.previousId = prev_node_list
        nodePrev.nodeId = str(node.id)
        nodePrev.save()