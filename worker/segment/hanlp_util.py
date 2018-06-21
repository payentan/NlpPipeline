import pytest
from pyhanlp import *
from domain.persist import *
import datetime
import json

from domain.persist import *
from domain.dao import *

@pytest.fixture
def hanlp_crf(request, nlp_ctx):
    tid = request.config.getoption('tid')
    nlp_ctx.text.load(tid)
    seg = HanLP.newSegment('crf')
    seg.enableOffset(True)
    #text = TextCol.objects(id=tid)
    #for t in text:
    terms = seg.seg(nlp_ctx.text.content)
    request.addfinalizer(
        lambda :
        nlp_ctx.segment.save(tid, 'hanlp', 'crf', {}, terms,
            lambda t: (t.word, str(t.nature), t.offset)
            )
    )
    return terms