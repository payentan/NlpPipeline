import pytest
from pyhanlp import *
from domain.persist import *
import datetime
import json

from domain.persist import *
from domain.dao import *

@pytest.fixture
def hanlp_nn(request):
    tid = request.config.getoption('tid')
    text = TextCol.objects(id=tid)
    for t in text:
        words = HanLP.parseDependency(t.content).iterator()
        request.addfinalizer(
            lambda :
            NodeDependency(tid, 'hanlp', 'nn', {}, words,
                lambda w: (w.NAME, w.LEMMA, w.CPOSTAG, w.POSTAG, w.HEAD.ID, w.DEPREL)
                )
        )
        return words