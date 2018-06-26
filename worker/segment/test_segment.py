import pytest
from worker.segment.hanlp_util import *
from worker.segment.jieba_util import *
from worker.segment.spacy_util import *
from worker.segment.nlpir_util import *

class TestSegment(object):

    def test_hanlp_crf(self, hanlp_crf):
        pass

    def test_jieba_pseg(self, jieba_pseg):
        pass

    def test_spacy_std(self, spacy_std):
        pass
    
    def test_nlpir_default(self, nlpir_default):
        pass
        
if __name__=='__main__':
    pytest.main()
