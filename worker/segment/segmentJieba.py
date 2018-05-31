import pytest
import jieba
import jieba.posseg as pseg
import jieba.analyse
import datetime
import json

from domain.persist import *
from domain.dao import *

def jieba_segment_persist(tid, software, algorithm, parameters, terms):

    NodeSegment(tid, software, algorithm, parameters, terms,
                lambda t: (t.word, str(t.flag), 0)
                )

@pytest.fixture
def jieba_pseg(request):
    tid = request.config.getoption('tid')
    text = TextCol.objects(id=tid)
    
    for t in text:
        terms = jieba.posseg.cut(t.content)
        #def finalize():
        #    jieba_segment_persist(tid, 'jieba', 'pseg', {}, terms) 
        request.addfinalizer(
            lambda :
            NodeSegment(tid, 'jieba', 'pseg', {}, terms,
                lambda t: (t.word, str(t.flag), 0)
                )
        )
        return terms