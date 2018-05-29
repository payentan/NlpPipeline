import pytest
import jieba
import jieba.posseg as pseg
import jieba.analyse
import datetime
import json

from domain.persist import *

def jieba_segment_persist(tid, software, algorithm, parameters, terms):
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
        (seg.word, seg.nature, seg.offset) = (term.word, str(term.flag), 0)
        seg.save()
        term_list.append(str(seg.id))

    node.result = json.dumps({'segment' : term_list })
    node.save()

    nodePrev = NodePreviousCol()
    nodePrev.previousId = tid
    nodePrev.nodeId = str(node.id)
    nodePrev.save()

@pytest.fixture
def jieba_pseg(request):
    tid = request.config.getoption('tid')
    text = TextCol.objects(id=tid)
    
    for t in text:
        terms = jieba.posseg.cut(t.content)
        def finalize():
            jieba_segment_persist(tid, 'jieba', 'pseg', {}, terms) 
        request.addfinalizer(finalize)
        return terms