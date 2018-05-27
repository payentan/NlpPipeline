import pytest
from pyhanlp import *
from domain.persist import *
import datetime

def hanlp_segment_persist(terms):
    for term in terms:
        seg = Segment()
        seg.seq_id = 123
        (seg.word, seg.nature, seg.offset) = (term.word, str(term.nature), term.offset)
        seg.save()

@pytest.fixture
def hanlp_crf(request):
    tid = request.config.getoption('tid')
    seg = HanLP.newSegment('crf')
    seg.enableOffset(True)
    text = Text.objects(id=tid)
    for t in text:
        terms = seg.seg(t.content)
        def finalize():
            for term in terms:
                hanlp_segment_persist(terms) 
        request.addfinalizer(finalize)
        return terms

class TestSegment(object):
    def test_hanlp_crf(self, hanlp_crf):
        for term in hanlp_crf:
            print('{}\t{}\t{}'.format(term.word, term.nature, term.offset)) 

if __name__=='__main__':
    pytest.main()
