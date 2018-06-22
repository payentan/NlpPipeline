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
    ctx = nlp_ctx
    tid = request.config.getoption('tid')
    ctx.text.load(tid)
    
    terms = jieba.posseg.cut(ctx.text.content)
    request.addfinalizer(
        lambda :
        ctx.segment.save(tid, 'jieba', 'pseg', {}, terms,
            lambda t: (t.word, str(t.flag), 0)
            )
    )
    return terms