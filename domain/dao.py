import json
from domain.persist import *

class Node():
    def __init__(self, prev_node_list, software, algorithm, parameters, result):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result

class NodeSegment():
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