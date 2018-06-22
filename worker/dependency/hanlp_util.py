import pytest
from pyhanlp import *
from domain.persist import *
import datetime
import json

from domain.persist import *
from domain.dao import *

@pytest.fixture
def hanlp_nn(request, nlp_ctx):
    ctx = nlp_ctx
    tid = request.config.getoption('tid')
    ctx.text.load(tid)
    words = HanLP.parseDependency(ctx.text.content).iterator()
    request.addfinalizer(
        lambda :
        ctx.dependency.save(tid, 'hanlp', 'nn', {}, words,
            lambda w: (w.NAME, w.LEMMA, w.CPOSTAG, w.POSTAG, w.HEAD.ID, w.DEPREL)
            )
    )
    return words