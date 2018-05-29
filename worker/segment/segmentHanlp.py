import pytest
from pyhanlp import *
from domain.persist import *
import datetime
import json

def hanlp_segment_persist(tid, software, algorithm, parameters, terms):
    node = NodeCol()
    node.software = software
    node.algorithm = algorithm
    node.parameters = ''
    term_list = []

    seqId = 0
    for term in terms:
        seg = SegmentCol()
        seg.seqId = seqId
        seqId = seqId + 1
        (seg.word, seg.nature, seg.offset) = (term.word, str(term.nature), term.offset)
        seg.save()
        term_list.append(str(seg.id))

    node.result = json.dumps({'segment' : term_list })
    node.save()

    nodePrev = NodePreviousCol()
    nodePrev.previousId = tid
    nodePrev.nodeId = str(node.id)
    nodePrev.save()

@pytest.fixture
def hanlp_crf(request):
    tid = request.config.getoption('tid')
    seg = HanLP.newSegment('crf')
    seg.enableOffset(True)
    text = TextCol.objects(id=tid)
    for t in text:
        terms = seg.seg(t.content)
        def finalize():
            hanlp_segment_persist(tid, 'hanlp', 'cfg', {}, terms) 
        request.addfinalizer(finalize)
        return terms