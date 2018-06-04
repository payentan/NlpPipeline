import pytest
import spacy

from domain.dao import *

@pytest.fixture
def spacy_std(request):
    tid = request.config.getoption('tid')
    text = TextCol.objects(id=tid)
    
    nlp = spacy.load('en_core_web_sm')

    for t in text:

        doc = nlp('Apple is looking at buying U.K. startup for $1 billion')

        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)

        request.addfinalizer(
            lambda :
            NodeSegment(tid, 'spacy', 'std', {}, doc,
                lambda t: (t.text, str(t.pos), 0)
                )
        )
        return doc