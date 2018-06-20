import pytest
import gensim
import os
from gensim.models import KeyedVectors
from domain.persist import *
from domain.dao import *

@pytest.fixture
def gensim_word2vec(request):
    tid = request.config.getoption('tid')

    text = TextCol.objects(id=tid)
    for t in text:
        model = gensim.models.Word2Vec([t.content.split()], min_count=1)
        word_vectors = model.wv
        model.save(os.path.join(os.getcwd(), 'data/ksdklf.bin'))
        del model
        print(os.path.join(os.getcwd(), 'data/ksdklf.bin'))
        print(word_vectors['Apple'])
        #request.addfinalizer(
        #    lambda :
        #    NodeEmbedding("", 'gensim', 'word2vec', {}, '/tmp/modeksjd')
        #)
        return None