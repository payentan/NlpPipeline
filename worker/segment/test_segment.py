import pytest
from segmentHanlp import *
from segmentJieba import *

class TestSegment(object):
    def test_seg(self, jieba_pseg):
        #for term in jieba_pseg:
        #    print('{}\t{}\t'.format(term.word, term.flag)) 
        pass

if __name__=='__main__':
    pytest.main()
