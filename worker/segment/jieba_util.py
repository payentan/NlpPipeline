import pytest
import jieba
import jieba.posseg as pseg
import jieba.analyse
import datetime
import json

from domain.persist import *
from domain.dao import *

@pytest.fixture
def jieba_pseg(request, nlp_ctx):
    tid = request.config.getoption('tid')
    text = TextCol.objects(id=tid)
    
    for t in text:
        terms = jieba.posseg.cut(t.content)
        request.addfinalizer(
            lambda :
            NodeSegment(tid, 'jieba', 'pseg', {}, terms,
                lambda t: (t.word, str(t.flag), 0)
                )
        )
        return terms