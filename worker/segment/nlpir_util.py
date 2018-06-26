import pytest
import pynlpir
from domain.dao import *

@pytest.fixture
def nlpir_default(request, nlp_ctx):
    ctx = nlp_ctx
    tid = request.config.getoption('tid')
    ctx.text.load(tid)
    pynlpir.open()
    terms = pynlpir.segment(ctx.text.content)
    pynlpir.close()
    request.addfinalizer(
        lambda :
        ctx.segment.save(tid, 'nlpir', 'default', {}, terms,
            lambda t: (t[0], t[1], 0)
            )
    )
    return terms