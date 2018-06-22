import pytest
import gensim
import os
from gensim.models import KeyedVectors
from domain.persist import *
from domain.dao import *

@pytest.fixture
def gensim_word2vec(request, nlp_ctx):
    ctx = nlp_ctx
    tid = request.config.getoption('tid')
    ctx.text.load(tid)

    model = gensim.models.Word2Vec([ctx.text.content.split()], min_count=1)
    word_vectors = model.wv

    model_file = os.path.join(os.getcwd(), 'data/ksdklf.bin')
    model.save(model_file)

    ctx.embedding.save(tid, "gensim", "Word2vec", {}, model_file)

    del model
    print(word_vectors['Apple'])
    return None