import pytest
from pyhanlp import *
from domain.persist import *
import datetime

@pytest.fixture
def hanlp_crf(request):
    tid = request.config.getoption('tid')
    seg = HanLP.newSegment('crf')
    seg.enableOffset(True)
    text = Text.objects(id=tid)
    for t in text:
        return seg.seg(t.content)

class TestSegment(object):
    def test_hanlp_crf(self, hanlp_crf):
        for term in hanlp_crf:
            print('{}\t{}\t{}'.format(term.word, term.nature, term.offset)) 

if __name__=='__main__':
    pytest.main()
